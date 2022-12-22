# import os
# import time
# from celery import shared_task
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from portal import enum
# from portal.python.SharedOrderFunctions import sendEmailWithAttachment
# from portal.tasks import generate_zip

# # Create your tests here.

# @shared_task
# def executeDiffChecking():

# 	automated_testing = os.path.dirname(os.path.abspath(__file__)) #chefables v2

# 	def _handleFailure(driver, file_name, sheet_index, error=""):
# 		if not os.path.exists(f'{automated_testing}/testing-screenshots/{file_name}'):
# 			os.mkdir(f'{automated_testing}/testing-screenshots/{file_name}')

# 		driver.get_screenshot_as_file(f'{automated_testing}/testing-screenshots/{file_name}/{time.time_ns()}-{os.path.splitext(file_name)[0]}-sheetIdx-{sheet_index}{error}.png')
# 		with open(f'{automated_testing}/failures.txt', 'a') as file:
# 			file.write('\n')
# 			file.write(f'{file_name}-sheetIdx:{sheet_index}-{error}')

# 	def _handleSuccess(file_name, sheet_index):
# 		with open(f'{automated_testing}/successes.txt', 'a') as file:
# 			file.write('\n')
# 			file.write(f'{file_name}-sheetIdx:{sheet_index}')

# 	def _findDifference(driver, file_name, sheet_index):
# 		submitButton = WebDriverWait(driver, 15).until(
# 			EC.presence_of_element_located((By.NAME, "Find difference"))
# 		)
# 		submitButton.click()

# 		try:
# 			driver.switch_to.alert.accept()
# 			_handleSuccess(file_name, sheet_index)
# 		except:
# 			_handleFailure(driver, file_name, sheet_index)

# 	# chrome_options = Options()
# 	# chrome_options.add_argument("--headless")

# 	driver = webdriver.Chrome()
# 	# driver = webdriver.Chrome(options=chrome_options)
# 	driver.get('https://www.diffchecker.com/excel-compare/')
# 	originalDirectoryPath = os.fsencode(f'{automated_testing}/test_files/dev')
# 	changedDirectoryPath = os.fsencode(f'{automated_testing}/test_files/prod')

# 	originalExcelDocuments = sorted(list(filter(lambda val: os.fsdecode(os.path.splitext(val)[1]) == '.xlsx', os.listdir(originalDirectoryPath))))
# 	changedExcelDocuments = sorted(list(filter(lambda val: os.fsdecode(os.path.splitext(val)[1]) == '.xlsx', os.listdir(changedDirectoryPath))))

# 	for idx in range(len(originalExcelDocuments)): #each Excel doc
# 		inputs = WebDriverWait(driver, 4).until(
# 			EC.presence_of_all_elements_located((By.XPATH, "//input[@class='diff-input-header_fileInput__6v6Mq']"))
# 		)
# 		# load Excel docs into inputs
# 		inputs[0].send_keys(f'{os.fsdecode(originalDirectoryPath)}/{os.fsdecode(originalExcelDocuments[idx])}')
# 		inputs[1].send_keys(f'{os.fsdecode(changedDirectoryPath)}/{os.fsdecode(changedExcelDocuments[idx])}')

# 		_findDifference(driver, os.fsdecode(changedExcelDocuments[idx]), 0) #first (idx 0) sheet only

# 		sheetNameSelects = WebDriverWait(driver, 15).until(
# 			EC.presence_of_all_elements_located((By.XPATH, "//select[@class='excel-input_sheetSelect__p7MmN diffResult']"))
# 		)
# 		sheet_idx = 1
# 		optionsLeft = sheetNameSelects[0].find_elements(By.TAG_NAME, "option")
# 		optionsRight = sheetNameSelects[1].find_elements(By.TAG_NAME, "option")
# 		if len(optionsLeft) == len(optionsRight):
# 			while sheet_idx < len(optionsLeft):  #each sheet after the first
# 				sheetNameSelects[0].click()
# 				optionsLeft[sheet_idx].click()

# 				sheetNameSelects[1].click()
# 				optionsRight[sheet_idx].click()

# 				_findDifference(driver, os.fsdecode(changedExcelDocuments[idx]), sheet_idx)
# 				sheet_idx += 1
# 		else:
# 			_handleFailure(driver=driver, file_name=os.fsdecode(changedExcelDocuments[idx]), sheet_index=sheet_idx, error="NUM SHEETS MISMATCH")

# 		print("workbook complete")
# 	print("script finished executing")
# 	attachment = open(f'{automated_testing}/failures.txt', 'rb')

# 	sendEmailWithAttachment("Diff Checking Complete", "diff checking is complete", attachment, "failures.txt", enum.DEV_EMAILS)