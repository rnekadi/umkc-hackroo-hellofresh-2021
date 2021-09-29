"""
Author :  Raju Nekadi
Description: This file is to define main module to perform etl.

"""

import src.config.arg as arg
from src.modules.executor import *

if __name__=="__main__":
	"""Main  ETL module script definition.
	:return: None
	"""
	try:
		logger.info("Recipe ETL Process has been Started !!!")
		arg.parser.add_argument('task', type=str, help='Name of the task need to perform')
		args, _ = arg.parser.parse_known_args()
		task_name = args.task
		etl = Executor(task_name)
		etl.run()
	except Exception as e:
		logger.info("Failed to load input args!!!")
		logger.exception("Error in main function " + str(e))

