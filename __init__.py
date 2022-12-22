import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def executeDiffChecking():
	def _handleFailure(driver, file_name, sheet_index, error=""):
		if not os.path.exists(f'./screenshots/{file_name}'):
			os.mkdir(f'./screenshots/{file_name}')

		driver.get_screenshot_as_file(f'./screenshots/{file_name}/{time.time_ns()}-{os.path.splitext(file_name)[0]}-sheetIdx-{sheet_index}{error}.png')
		with open('./failures.txt', 'a') as file:
			file.write('\n')
			file.write(f'{file_name}-sheetIdx:{sheet_index}-{error}')

	def _handleSuccess(file_name, sheet_index):
		with open('./successes.txt', 'a') as file:
			file.write('\n')
			file.write(f'{file_name}-sheetIdx:{sheet_index}')

	def _findDifference(driver, file_name, sheet_index):
		submitButton = WebDriverWait(driver, 15).until(
			EC.presence_of_element_located((By.NAME, "Find difference"))
		)
		submitButton.click()

		try:
			driver.switch_to.alert.accept()
			_handleSuccess(file_name, sheet_index)
		except:
			_handleFailure(driver, file_name, sheet_index)



	driver = webdriver.Chrome()
	driver.get('https://www.diffchecker.com/excel-compare/')

	originalDirectoryPath = os.fsencode('/Users/chefables_imac/Desktop/automated-testing/test_files/dev')
	changedDirectoryPath = os.fsencode('/Users/chefables_imac/Desktop/automated-testing/test_files/prod')

	originalExcelDocuments = sorted(list(filter(lambda val: os.fsdecode(os.path.splitext(val)[1]) == '.xlsx', os.listdir(originalDirectoryPath))))
	changedExcelDocuments = sorted(list(filter(lambda val: os.fsdecode(os.path.splitext(val)[1]) == '.xlsx', os.listdir(changedDirectoryPath))))

	for idx in range(len(originalExcelDocuments)): #each Excel doc
		inputs = WebDriverWait(driver, 4).until(
			EC.presence_of_all_elements_located((By.XPATH, "//input[@class='diff-input-header_fileInput__6v6Mq']"))
		)
		# load Excel docs into inputs
		inputs[0].send_keys(f'{os.fsdecode(originalDirectoryPath)}/{os.fsdecode(originalExcelDocuments[idx])}')
		inputs[1].send_keys(f'{os.fsdecode(changedDirectoryPath)}/{os.fsdecode(changedExcelDocuments[idx])}')

		_findDifference(driver, os.fsdecode(changedExcelDocuments[idx]), 0) #first (idx 0) sheet only

		sheetNameSelects = WebDriverWait(driver, 15).until(
			EC.presence_of_all_elements_located((By.XPATH, "//select[@class='excel-input_sheetSelect__p7MmN diffResult']"))
		)
		sheet_idx = 1
		optionsLeft = sheetNameSelects[0].find_elements(By.TAG_NAME, "option")
		optionsRight = sheetNameSelects[1].find_elements(By.TAG_NAME, "option")
		if len(optionsLeft) == len(optionsRight):
			while sheet_idx < len(optionsLeft):  #each sheet after the first
				sheetNameSelects[0].click()
				optionsLeft[sheet_idx].click()

				sheetNameSelects[1].click()
				optionsRight[sheet_idx].click()

				_findDifference(driver, os.fsdecode(changedExcelDocuments[idx]), sheet_idx)
				sheet_idx += 1
		else:
			_handleFailure(driver=driver, file_name=os.fsdecode(changedExcelDocuments[idx]), sheet_index=sheet_idx, error="NUM SHEETS MISMATCH")

		print("workbook complete")
	print("script finished executing")
	# try:
	# 	sender = "tbhdevtools@gmail.com" # replace with sender's email address
	# 	receiver = "tbhdevtools@gmail.com" # replace with receiver's email address
	# 	password = "GdGFT9&dyc8b6@tpE6NB48NY" # replace with your password
	# 	host = 'smtp.gmail.com' # replace with your host, e.g. gmail = smtp.gmail.com
	# 	port = 465 # replace with your port, e.g. gmail = 465

	# 	s = smtplib.SMTP_SSL(host, port)
	# 	s.login(sender, password)

	# 	html_mail = """<meta charset="UTF-8">
	# 	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	# 	<meta name="viewport" content="width=device-width, initial-scale=1">
	# 	<title>Test1</title>
	# 	<h1> Email Title </h1>
	# 	<p> Email Content </p>
	# 	"""

	# 	msg = MIMEMultipart('alternative')
	# 	msg['Subject'] = f"Test Automated Email" # replace with your subject 
	# 	msg['From'] = sender
	# 	msg['To'] = receiver

	# 	html = html_mail
	# 	part2 = MIMEText(html, 'html')

	# 	msg.attach(part2)

	# 	s.sendmail(sender, receiver, msg.as_string())

	# 	s.quit()
	# except:
	# 	print("emailing failed")

executeDiffChecking()