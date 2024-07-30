import boto3, json
import modules.envReader as envReader
from loguru import logger
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from models.articles import Articles
from models.zhilserviceUsers import ZhilserviceUsers
from models.accounts import Accounts
from models.orders import Orders
from models.personalAccounts import PersonalAccounts

credents = envReader.init()

DB_USERNAME = credents.get('DB_USERNAME', '')
DB_PASSWORD = credents.get('DB_PASSWORD', '')
DB_HOST = credents.get('DB_HOST', '')
DB_NAME = credents.get('DB_NAME', '')

AWS_ACCESS_KEY_ID = credents.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = credents.get('AWS_SECRET_ACCESS_KEY', '')
BUCKET_NAME = credents.get('BUCKET_NAME', '')
FILENAME = credents.get('FILENAME', '')

TOPIC_ARN = credents.get('TOPIC_ARN', '')

tables = (Articles, ZhilserviceUsers, Accounts, Orders, PersonalAccounts)
st_response_json = {
	'status': 'error',
	'err_description': ''		
}

def __send_notification(err_description):
	response_json = st_response_json.copy()

	try:
		sns_client = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
		sns_client.publish(
			TopicArn=TOPIC_ARN,
			Message=f'ERROR: {err_description}',
			Subject='Failed db copy'
		)

		response_json['status'] = 'success'
		response_json['message'] = 'Notification sent!'

	except Exception as e:
		response_json['err_description'] = str(e)

	return response_json

def __saving(data):
	response_json = st_response_json.copy()

	try:
		s3_client = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')
		s3_bucket = s3_client.Bucket(BUCKET_NAME)

		s3_bucket.put_object(Key=FILENAME, Body=json.dumps(data))
		response_json['status'] = 'success'

	except Exception as e:
		response_json['err_description'] = str(e)

	return response_json

def __db_connection():
	connection_str = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
	engine = create_engine(connection_str, echo=False)
	session = Session(engine)
	return session

def lambda_handler(event, context):
	response_json = st_response_json.copy()

	try:
		connection = __db_connection()

		all_table_data = {}
		for table in tables:
			tablename = table.__tablename__
			all_table_data[tablename] = {'table_describe': None, 'rows': []}

			stmt = select(table).where(table.id != 0)
			for row in connection.scalars(stmt):
				data = row.to_json()
				all_table_data[tablename]['rows'].append(data)

			descr_stmt = text(f'DESCRIBE {tablename};')
			descr = connection.execute(descr_stmt).fetchall()
			all_table_data[tablename]['table_describe'] = [{column: value for column, value in zip(['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'], row)} for row in descr]

		# logger.info(all_table_data)
		saving = __saving(all_table_data)
		response_json = saving.copy()
	
	except Exception as e:
		response_json['err_description'] = str(e)

	finally:
		if response_json['status'] == 'error':
			err_description = response_json['err_description']
			send_notification = __send_notification(err_description)
			logger.info(send_notification)

	return

