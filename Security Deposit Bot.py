from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import openpyxl as excel
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill, Font
# import csv
import time
import string
import os

import pandas as pd
import numpy as np

import tkinter as tk

# -----------------------------
app_start_time = time.time()
# -----------------------------

# initialize the object
SD_Robot = webdriver.Chrome()
SD_Robot.maximize_window()
hold = WebDriverWait(SD_Robot,45)


mouse_kyb = ActionChains(SD_Robot)

cycle_status = [0,0]


def ax_spinner() :
    WebDriverWait(SD_Robot, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "loadingOff")))

def siebel_spinner() :
    WebDriverWait(SD_Robot, 30, poll_frequency=0.2).until(
        EC.invisibility_of_element_located((By.ID, "maskoverlay")))


    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # WebDriverWait(driver, 30, poll_frequency=0.2).until(
    #     EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, "#maskoverlay[style*='display:none']")
    #     )
    # )
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # while True :
    #     loading = hold.until(EC.presence_of_element_located((By.ID, "maskoverlay"))).get_attribute("style")
    #     if "block" in loading :
    #         continue
    #
    #     if "none" in loading :
    #         time.sleep(0.5)
    #         break
    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

Siebel_tab = ""


def siebel_login(username,password) :
    global Siebel_tab

    SD_Robot.get("Siebel URL")

    SD_Robot.implicitly_wait(30)

    Siebel_tab = SD_Robot.window_handles[0]

    # Enter UserName
    hold.until(EC.visibility_of_element_located((By.ID,"s_swepi_1"))).send_keys(username)
    # Enter Password
    hold.until(EC.visibility_of_element_located((By.ID, "s_swepi_2"))).send_keys(password)
    # Press To log in
    hold.until(EC.element_to_be_clickable((By.ID, "s_swepi_22"))).click()


    try :
        time.sleep(1)
        hold.until(EC.alert_is_present())
        time.sleep(1)
        SD_Robot.switch_to.alert.accept()
        time.sleep(1)
        siebel_spinner()
        time.sleep(1)

    except :
        SD_Robot.refresh()

        try :
            SD_Robot.implicitly_wait(30)

            # Enter UserName
            hold.until(EC.visibility_of_element_located((By.ID, "s_swepi_1"))).send_keys(username)
            # Enter Password
            hold.until(EC.visibility_of_element_located((By.ID, "s_swepi_2"))).send_keys(password)
            # Press To log in
            hold.until(EC.element_to_be_clickable((By.ID, "s_swepi_22"))).click()


        except :
            siebel_spinner()
            SD_Robot.refresh()
            siebel_spinner()

            mouse_kyb.key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('x').key_up(Keys.SHIFT).key_up(
                Keys.CONTROL).perform()

            siebel_spinner()
            SD_Robot.refresh()

            SD_Robot.implicitly_wait(30)

            # Enter UserName
            hold.until(EC.visibility_of_element_located((By.ID, "s_swepi_1"))).send_keys(username)
            # Enter Password
            hold.until(EC.visibility_of_element_located((By.ID, "s_swepi_2"))).send_keys(password)
            # Press To log in
            hold.until(EC.element_to_be_clickable((By.ID, "s_swepi_22"))).click()


        finally:
            time.sleep(1)
            hold.until(EC.alert_is_present())
            time.sleep(1)
            SD_Robot.switch_to.alert.accept()
            time.sleep(1)
            siebel_spinner()
            time.sleep(1)

    # Press Service Request
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s_sctrl_tabScreen']/ul/li[8]"))).click()
    siebel_spinner()
    time.sleep(1.5)

# -------------------------------------------------------------------------
AX_tab = ""
# -------------------------------------------------------------------------

def ax_login(username,password) :
    global AX_tab

    time.sleep(0.5)
    # Open a new tab using JavaScript.
    SD_Robot.execute_script("window.open('APP URL');")
    time.sleep(0.5)

    # Switch to second tab ( AX ).
    SD_Robot.switch_to.window(   SD_Robot.window_handles[-1]   )
    time.sleep(1)
    AX_tab = SD_Robot.window_handles[-1]


    # Check Point To Move.
    hold.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='footer']//p")))

    # Enter UserName.
    hold.until(EC.visibility_of_element_located((By.ID,"j_username"))).send_keys(username)
    # Enter Password.
    hold.until(EC.visibility_of_element_located((By.ID, "j_password"))).send_keys(password)

    # Press Ok To log in.
    hold.until(EC.element_to_be_clickable((By.CLASS_NAME, "ButtonStandard"))).click()
    time.sleep(1)

    # Press Debtors and creditors.
    hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "Debtors and creditors"))).click()
    time.sleep(1)


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


def full_ticket_cycle(SR_Num) :

    global Siebel_tab, AX_tab , cycle_status

    SD_Robot.switch_to.window(Siebel_tab)
    time.sleep(0.25)

    # Insert SR number to the Query Field.
    hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
     "#s_S_A6_div > div.siebui-screen-hp-applet > form > div > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td.siebui-form-data > table > tbody > tr > td > input"))).send_keys(SR_Num)

    # Press Enter
    time.sleep(0.25)
    mouse_kyb.send_keys(Keys.ENTER).perform()
    siebel_spinner()

    # Found the SR first.
    found_sr = hold.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='s_2_l']/tbody/tr")))
    if len(found_sr) == 1 :
        return "SR Number Is Not Valid."


    assigned_sr = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='a_1']/div/table/tbody/tr[5]/td[9]/div/input")))
    value_assigned_sr = str(SD_Robot.execute_script("return arguments[0].value;", assigned_sr)).strip()

    if value_assigned_sr != "Assigned" :
        return f"SR Status is not Assigned"


    # Press On SR hyperlink to enter.
    sr_element = hold.until(EC.element_to_be_clickable((By.CSS_SELECTOR, r"#\31 _s_2_l_SR_Number")))
    # left click by mouse to enter SR page.
    mouse_kyb.move_to_element(sr_element).click().perform()
    siebel_spinner()


    # Press on Smart Script.
    time.sleep(0.75)
    smart_script = hold.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#s_1_1_257_0_Ctrl")))
    SD_Robot.execute_script("arguments[0].click();", smart_script)
    time.sleep(0.5)
    siebel_spinner()


    # Data Scraping.
    # ---------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    account_from = hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                       "#SSQuestionList > table:nth-child(1) > tbody > tr > td > span.scField > input")))
    value_account_from = str(SD_Robot.execute_script("return arguments[0].value;", account_from)).strip()
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    account_to = hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                        "#SSQuestionList > table:nth-child(2) > tbody > tr > td > span.scField > input")))
    value_account_to = str(SD_Robot.execute_script("return arguments[0].value;", account_to)).strip()
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    reference_code = hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                        "#SSQuestionList > table:nth-child(3) > tbody > tr > td > span.scField > input")))
    value_reference_code = str(SD_Robot.execute_script("return arguments[0].value;", reference_code)).strip()
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # date = hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
    #                     "#SSQuestionList > table:nth-child(4) > tbody > tr > td > span.scField > input")))
    # value_date_siebel = str(SD_Robot.execute_script("return arguments[0].value;", date)).strip()
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    comment = hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                         "#SSQuestionList > table:nth-child(5) > tbody > tr > td > span.scField > input")))
    value_comment = str(SD_Robot.execute_script("return arguments[0].value;", comment)).strip()
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    sd_amount = hold.until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                          "#SSQuestionList > table:nth-child(6) > tbody > tr > td > span.scField > input")))
    value_sd_amount = str(SD_Robot.execute_script("return arguments[0].value;", sd_amount)).strip()
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------
    acc_from = ""
    for strange_1 in value_account_from :
        if strange_1.isdigit() or "." in strange_1 :
            acc_from += strange_1

    value_account_from = acc_from
    # ---------------------------------------------------
    acc_to = ""
    for strange_2 in value_account_to:
        if strange_2.isdigit() or "." in strange_2:
            acc_to += strange_2

    value_account_to = acc_to
    # ---------------------------------------------------
    # ---------------------------------------------------

    if len(value_account_from) not in (10, 11) or len(value_account_to) not in (10, 11):
        return "Wrong SS Account Number"

    if len(value_reference_code) <= 8   :
        return "Wrong SS Reference Code."

    if len(value_sd_amount) == 0   :
        return "Wrong SS SD Move Amount."
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Press Finish Smart Script.
    time.sleep(0.2)
    finish_btn = hold.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#s_2_1_5_0_Ctrl")))
    SD_Robot.execute_script("arguments[0].click();", finish_btn)
    siebel_spinner()
    time.sleep(0.2)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # AX Part.

    SD_Robot.switch_to.window(AX_tab)
    time.sleep(0.1)

    # Press Financial overview Button
    hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "Financial overview"))).click()
    time.sleep(0.05)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Validate account ( TO ), first step.
    hold.until(EC.visibility_of_element_located((By.ID, "CS_CODE"))).send_keys(value_account_to)

    # Press Search.
    hold.until(EC.element_to_be_clickable((By.ID, "debtorCreditorCriteria_formTag_CUSTOMER_SEARCH_BUTTON"))).click()
    time.sleep(0.15)
    ax_spinner()

    # If account appeared, it's mean that the account is located, else it's mean the account number not exist.
    data_bar = hold.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#kibar > table > tbody > tr > td > span")))
    returned_value_1 = False

    for item in data_bar :
        if str(item.text).strip() == value_account_to :
            returned_value_1 = True
            break

    if returned_value_1 == False :
        return f"Account Number {value_account_to},Not Found"

    # ------------------------------------------------------------------------------------------------------------------
    # Validate account ( From ), Second step.
    time.sleep(1)
    hold.until(EC.visibility_of_element_located((By.ID, "CS_CODE"))).clear()
    time.sleep(0.75)
    hold.until(EC.visibility_of_element_located((By.ID, "CS_CODE"))).send_keys(value_account_from)

    # Press Search.
    hold.until(EC.element_to_be_clickable((By.ID, "debtorCreditorCriteria_formTag_CUSTOMER_SEARCH_BUTTON"))).click()
    time.sleep(0.15)
    ax_spinner()

    # If account appeared, it's mean that the account is located, else it's mean the account number not exist.
    data_bar_2 = hold.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#kibar > table > tbody > tr > td > span")))
    returned_value_2 = False

    for item_2 in data_bar_2 :
        if str(item_2.text).strip() == value_account_from :
            returned_value_2 = True
            break

    if returned_value_2 == False :
        return f"Account Number {value_account_from},Not Found"
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # Press Deposit
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='financialOverviewTab_tablist']/div[4]/div/div[2]"))).click()
    ax_spinner()
    time.sleep(0.15)

    # Clear date from-11.
    deposits_field = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='Period_From_Field_Deposits']")))
    SD_Robot.execute_script("arguments[0].value = '';", deposits_field)
    ax_spinner()
    time.sleep(0.25)

    # Press Radio BTN of Both.
    both_items_radio = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='DOC_STATUS_RADIOBUTTON_GROUP'][3]")))
    if not both_items_radio.is_selected() :
        both_items_radio.click()
        ax_spinner()
    time.sleep(0.25)

    # Press search.
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='finOverviewDepositCriteriaForm_formTag_DEPOSITS_SEARCH_BUTTON']"))).click()
    ax_spinner()
    time.sleep(0.25)

    # -----------------------------------------------------------
    # Re Fetch Security Deposits.
    # -----------------------------------------------------------
    paid_list = []
    refunded_list = []

    all_deposits = hold.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='CTX_DEPOSITS_TABLE']/tbody[2]/tr")))

    for one_deposit in all_deposits :
        if "Refunded" in one_deposit.text :
            refunded_list.append(one_deposit.text)

        if "Paid" in one_deposit.text:
            paid_list.append(one_deposit.text)

    # -----------------------------------------------------------
    # -----------------------------------------------------------
    if len(paid_list) == 0 :
        return f"Account Number {value_account_from}, has no SD to be moved."

    targeted_sd = []

    for sd_row in paid_list :
        if value_reference_code in sd_row and value_sd_amount in sd_row:
            targeted_sd.append(sd_row)
            break

    if len(targeted_sd) <= 0 :
        return f"SD Not Found, Or Maybe Refunded."

    if len(targeted_sd) > 1 :
        return f"Please Check the Account #{value_account_from}, As The SD founded {len(targeted_sd)} Times."
    # -----------------------------------------------------------
    # -----------------------------------------------------------

    # Press financials
    time.sleep(0.15)
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='financialOverviewTab_tablist']/div[4]/div/div[1]"))).click()
    ax_spinner()
    time.sleep(0.15)


    # Clear date field.
    date_from_element = hold.until(EC.visibility_of_element_located((By.ID, "Period_From_Field_Transactions")))
    SD_Robot.execute_script("arguments[0].value = '';", date_from_element)
    time.sleep(0.15)


    # Press to search after date crystal clear.
    hold.until(EC.element_to_be_clickable((By.ID, "financialOverviewDocumentsPane_formTag_TRANSACTIONS_SEARCH_BUTTON"))).click()
    ax_spinner()
    time.sleep(0.25)


    def sd_in_home() :
        """Check if the SD exist and appeared in the home page or not
        and how many times appeared ?
        it is aim to avoid handling Reverse Deposit Payment"""

        try :
            appeared_sd_count = WebDriverWait(SD_Robot, 10).until(EC.visibility_of_all_elements_located((By.XPATH,
                                 f"//td[contains(text() , '{value_reference_code.strip()}')]")))

            if len(appeared_sd_count) == 1 :
                return 1

            elif len(appeared_sd_count) != 1 :
                return 2

        except :
            return 0


    if sd_in_home() == 0 :
        return "The SD not Found in the main AX page."

    if sd_in_home() == 2 :
        return f"Please check SD status, maybe reversed or duplicated."


    # If Passed, that mean the SD is appeared.

    # -----------------------------------------------------------
    # -----------------------------------------------------------
    # -----------------------------------------------------------
    def get_comment(element,trx_name) :
        """FX to get the comment of the SD."""
        ax_spinner()
        details_btn = element.find_elements(By.TAG_NAME, "td")[1].find_element(By.TAG_NAME, "input")
        SD_Robot.execute_script("arguments[0].click();", details_btn)
        ax_spinner()
        time.sleep(0.1)

        try :
            window_Reference_code = hold.until(EC.visibility_of_element_located((By.XPATH,
                    "//*[@id='financialTransactionDetails_formTag_SectionContent']/table[1]/tbody/tr[2]/td[2]/div/span"))).text

            if window_Reference_code == trx_name :
                paper_comment = hold.until(EC.visibility_of_element_located((By.XPATH,
                         "//*[@id='financialTransactionDetails_formTag_SectionContent']/table[1]/tbody/tr[13]/td[2]/div/span"))).text

                time.sleep(0.50)
                ax_spinner()
                close_btn = hold.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='financialTransactionDetails_formTag_SuCancelButton']")))
                SD_Robot.execute_script("arguments[0].click();", close_btn)
                ax_spinner()
                time.sleep(0.25)

                return paper_comment


        except :
            return 0

    # -----------------------------------------------------------
    # -----------------------------------------------------------
    all_rows = hold.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='CTX_TRANSACTIONS_TABLE']/tbody/tr")))
    time.sleep(0.2)

    comment_text = ""

    ax_date_text = ""

    for each_one in all_rows :

        transaction_name = each_one.find_elements(By.TAG_NAME, "td")[2].text

        if transaction_name == value_reference_code.strip() :
            time.sleep(0.5)

            ax_date_text = each_one.find_elements(By.TAG_NAME, "td")[3].text
            time.sleep(0.10)

            # Give the FX element to get the comment.
            # Give the FX TRX name to ensure that the FX opened the correct Row details.
            comment_fx = get_comment(each_one,transaction_name)
            if comment_fx == 0 :
                return "Details Window Got Error"

            comment_text = comment_fx
            time.sleep(0.5)

            radio_btn = each_one.find_element(By.XPATH, ".//td[1]/input[@id='TCB_CTX_TRANSACTIONS_TABLE']")
            if not radio_btn.is_selected() :
                radio_btn.click()
                ax_spinner()
                time.sleep(0.5)
                break


    hold.until(EC.element_to_be_clickable((By.XPATH,
                  "//*[@id='financialOverviewDocumentsPane_formTag_TRANSACTION_REVERSE_BUTTON']"))).click()
    ax_spinner()
    time.sleep(0.25)


    def correct_sd() :
        """The FX is aim to ensure that i am in the right SD Reference code."""

        try :
            matched_reverse_page = WebDriverWait(SD_Robot, 10).until(EC.visibility_of_all_elements_located((By.XPATH,
                                      f"//td[contains(text() , '{value_reference_code.strip()}')]")))

            if len(matched_reverse_page) == 2 :
                return True

            else :
                return False

        except :
            return False

    if not correct_sd() :
        return f"Internal Reverse Page is issued."

    # If Passed, that mean the SD is appeared normally inside the reverse action page.

    # -----------------------------------------------------
    # -----------------------------------------------------
    ax_spinner()

    # select from Drop Menu
    drop_menu = hold.until(EC.element_to_be_clickable((By.CLASS_NAME, "SelectDdlL")))
    choice = Select(drop_menu)
    choice.select_by_visible_text("Closed account number")
    ax_spinner()
    time.sleep(0.15)

    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='SUSPEND_DDEBIT']"))).click()
    ax_spinner()
    time.sleep(0.15)


    comment_field = hold.until(EC.visibility_of_element_located((By.ID, "REMARK")))
    comment_string = f"{comment_text} to ac##{value_account_to}"
    SD_Robot.execute_script(f"arguments[0].value = '{comment_string}';", comment_field)
    ax_spinner()
    time.sleep(0.15)


    # Press Save.
    save_btn = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='reverseTransactionWorkflow_formTag_SaveButton']")))
    SD_Robot.execute_script("arguments[0].click();", save_btn)
    ax_spinner()
    time.sleep(0.5)


    # Close Window of ( Confirm Transaction ).
    confirm_window_close = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='confirmTransactionForm_formTag_CLOSE_BUTTON']")))
    SD_Robot.execute_script("arguments[0].click();", confirm_window_close)
    ax_spinner()
    time.sleep(0.75)

    # -----------------------------------------------------
    # Check After Reverse Action.

    # Press Deposit
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='financialOverviewTab_tablist']/div[4]/div/div[2]"))).click()
    ax_spinner()
    time.sleep(1.5)

    # Clear date from-11.
    deposits_field = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='Period_From_Field_Deposits']")))
    SD_Robot.execute_script("arguments[0].value = '';", deposits_field)
    ax_spinner()
    time.sleep(0.50)

    # Press Radio BTN of Both.
    both_items_radio = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='DOC_STATUS_RADIOBUTTON_GROUP'][3]")))
    if not both_items_radio.is_selected() :
        both_items_radio.click()
        ax_spinner()
    time.sleep(0.50)

    # Press search.
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='finOverviewDepositCriteriaForm_formTag_DEPOSITS_SEARCH_BUTTON']"))).click()
    ax_spinner()
    time.sleep(0.50)


    all_deposits = hold.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='CTX_DEPOSITS_TABLE']/tbody[2]/tr")))

    for line in all_deposits :
        if value_reference_code in line.text and value_sd_amount in line.text and "Refunded" in line.text :
            cycle_status[0] = 1
            break

    if cycle_status[0] != 1 :
        return "Reverse SD Action is Failed please review the Steps again, ( Refund Phase )."


    # -------------------------------------------------------------------------------------------
    # Go to Next Step ( account to ).
    # -------------------------------------------------------------------------------------------
    ax_spinner()
    time.sleep(0.50)
    hold.until(EC.visibility_of_element_located((By.ID, "CS_CODE"))).clear()
    time.sleep(0.50)
    hold.until(EC.visibility_of_element_located((By.ID, "CS_CODE"))).send_keys(value_account_to)
    time.sleep(0.50)
    ax_spinner()

    # Press Search.
    hold.until(EC.element_to_be_clickable((By.ID, "debtorCreditorCriteria_formTag_CUSTOMER_SEARCH_BUTTON"))).click()
    ax_spinner()
    time.sleep(2)


    try:
        # Press Payment transaction.
        WebDriverWait(SD_Robot, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "Payment transaction"))).click()
        ax_spinner()
        time.sleep(1)

    except :
        # Press Transactions.
        hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transactions"))).click()
        ax_spinner()
        time.sleep(1)

        # Press Payment transaction.
        hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "Payment transaction"))).click()
        ax_spinner()
        time.sleep(1)


    # Press Incoming deposit payments.
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='paymentTransactions_tablist']/div[4]/div/div[2]"))).click()
    ax_spinner()
    time.sleep(1)

    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------
    # Fill SD Data at received account.
    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------

    # Fill Reference code ( 1 ).
    reference_code_2 = hold.until(EC.visibility_of_element_located((By.XPATH,
                         "//*[@id='overviewSectionContent']/table[1]/tbody/tr[2]/td[2]/div/input[@id='TRANSACTION_REFNUM']")))
    SD_Robot.execute_script(f"arguments[0].value = '{value_reference_code}';", reference_code_2)
    ax_spinner()
    time.sleep(0.25)


    # Fill GL code ( 2 ).
    gl_code = hold.until(EC.visibility_of_element_located((By.XPATH,
                      "//*[@id='overviewSectionContent']/table[1]/tbody/tr[7]/td[2]/div/input[@id='GL_ACCOUNT']")))
    SD_Robot.execute_script("arguments[0].value = '';", gl_code)
    time.sleep(0.5)
    SD_Robot.execute_script(f"arguments[0].value = '000012205200000000000000000000';", gl_code)
    ax_spinner()
    time.sleep(0.25)


    # Fill Comment ( 3 ).
    comment_tab = hold.until(EC.visibility_of_element_located((By.XPATH,
                     "//*[@id='overviewSectionContent']/table[1]/tbody/tr[9]/td[2]/div/input[@id='REMARK']")))
    SD_Robot.execute_script(f"arguments[0].value = '{comment_text}';", comment_tab)
    ax_spinner()
    time.sleep(0.25)


    # Fill Amount ( 4 ).
    amount_tab = hold.until(EC.visibility_of_element_located((By.XPATH,
                  "//*[@id='overviewSectionContent']/table[1]/tbody/tr[8]/td[2]/div/input[@id='CASHAMOUNT_FIELD']")))
    SD_Robot.execute_script("arguments[0].value = '';", amount_tab)
    time.sleep(0.5)
    SD_Robot.execute_script(f"arguments[0].value = '{value_sd_amount}';", amount_tab)
    ax_spinner()
    time.sleep(0.25)

    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------

    def date_step(param_date):
        """FX to return the pure date"""

        # Normalize to remove time component
        today = pd.Timestamp.today().normalize()
        date_range = pd.date_range(end=today, periods=365)
        date_series = pd.Series(date_range)

        # -----------------------------------------------------------
        # -----------------------------------------------------------

        def date_machine():
            year = param_date[-4:].strip()
            month = param_date[:3].strip()

            day = "".strip()

            for char in param_date:
                if char.isdigit():
                    day += char
                if char == ",":
                    break

            if len(day) == 1:
                day = f"0{day}"

            # Convert month abbreviation to number ( dictionary ).
            month_map = {
                "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
                "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
            }

            month = month_map[month]

            return pd.to_datetime(f"{year}-{month}-{day}")

        convert_date_format = date_machine()

        # -----------------------------------------------------------
        # -----------------------------------------------------------

        if convert_date_format in date_series.values :
            return 1

    fetch_date = date_step(ax_date_text)

    if fetch_date == 1 :
        # Fill Reference date ( 5 ).

        reference_date_field = hold.until(EC.visibility_of_element_located((By.XPATH,
                "//*[@id='overviewSectionContent']/table[1]/tbody/tr[2]/td[5]/div/input[@id='Reference_Date_Field_Incoming_Deposit_Payments']")))

        SD_Robot.execute_script("arguments[0].value = '';", reference_date_field)
        time.sleep(0.5)
        SD_Robot.execute_script(f"arguments[0].value = '{ax_date_text}';", reference_date_field)
        ax_spinner()
        time.sleep(0.75)

    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------

    # Press Save.
    save_btn_2 = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='incomingDepositPayments_formTag_SAVE_BUTTON']")))
    SD_Robot.execute_script("arguments[0].click();", save_btn_2)
    ax_spinner()
    time.sleep(1)
    ax_spinner()

    # --------------------

    # Close Window of ( Confirm Transaction ).
    confirm_window_close_2 = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='confirmTransactionForm_formTag_CLOSE_BUTTON']")))
    SD_Robot.execute_script("arguments[0].click();", confirm_window_close_2)
    ax_spinner()
    time.sleep(1.5)
    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------

    # Press Financial overview Tab.
    hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "Financial overview"))).click()
    ax_spinner()
    time.sleep(1.25)
    # ------------------------------
    # Press Deposit
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='financialOverviewTab_tablist']/div[4]/div/div[2]"))).click()
    ax_spinner()
    time.sleep(1.5)
    # ------------------------------
    # Clear date from-112.
    deposits_field_2 = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='Period_From_Field_Deposits']")))
    SD_Robot.execute_script("arguments[0].value = '';", deposits_field_2)
    ax_spinner()
    time.sleep(1)
    # ------------------------------
    # ------------------------------
    # Press Radio BTN of Both.
    both_items_radio_2 = hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='DOC_STATUS_RADIOBUTTON_GROUP'][3]")))
    if not both_items_radio_2.is_selected():
        both_items_radio_2.click()
        ax_spinner()
        time.sleep(1)
    # ------------------------------
    # Press search.
    hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='finOverviewDepositCriteriaForm_formTag_DEPOSITS_SEARCH_BUTTON']"))).click()
    ax_spinner()
    time.sleep(1)

    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # Validate phase of the paid SD in second account.

    all_deposits_2 = hold.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='CTX_DEPOSITS_TABLE']/tbody[2]/tr")))

    for line_2 in all_deposits_2 :
        if value_reference_code in line_2.text and value_sd_amount in line_2.text and "Paid" in line_2.text :
            cycle_status[1] = 1
            break

    if cycle_status[1] != 1 :
        return "Reverse SD Action is Failed please review the Steps again, ( Paid Phase )."


    # Out from AX.
    time.sleep(1.5)
    hold.until(EC.element_to_be_clickable((By.XPATH,
        "//*[@id='form_formTag_SectionContent']/table/tbody/tr/td/input[@id='form_formTag_CLOSE_BUTTON']"))).click()
    time.sleep(1.5)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Ensure that you out from account and you in home page.

    try :
        ax_home_accounting_center = WebDriverWait(SD_Robot, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#content > div.header > h1 > span"))).text

        if "Home" not in ax_home_accounting_center and "Accounting Center" not in ax_home_accounting_center:

            # Press Home in nav bar.
            WebDriverWait(SD_Robot, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='hNavBar']/a[1]"))).click()

            ax_home_accounting_center = WebDriverWait(SD_Robot, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#content > div.header > h1 > span"))).text

            if "Home" not in ax_home_accounting_center and "Accounting Center" not in ax_home_accounting_center:
                return f"There is an issue in the home page of ax."

    except :
        # IF Error Occurred ( dimmed page or red line appeared )
        time.sleep(1)
        SD_Robot.refresh()
        time.sleep(1)
        SD_Robot.get("APP URL")

        # Check Point To Move.
        hold.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='footer']//p")))

        # Enter UserName.
        hold.until(EC.visibility_of_element_located((By.ID, "j_username"))).send_keys(ax_username)
        # Enter Password.
        hold.until(EC.visibility_of_element_located((By.ID, "j_password"))).send_keys(ax_password)

        # Press Ok To log in.
        hold.until(EC.element_to_be_clickable((By.CLASS_NAME, "ButtonStandard"))).click()
        time.sleep(1)

        # Press Debtors and creditors.
        hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "Debtors and creditors"))).click()
        time.sleep(3)

    # ------------------------------------------------------------------------------------------------------------------
    # Now You Are Ready To Siebel Phase.
    # ------------------------------------------------------------------------------------------------------------------
    SD_Robot.switch_to.window(Siebel_tab)
    time.sleep(2)

    # ------------------------------------------------------------------------------------------------------------------
    def more_info() :
        """Handling More Info Section"""
        # SD_Robot.execute_script("""
        #      arguments[0].value = 'SMS Sent';
        #      arguments[0].dispatchEvent(new Event('change'));
        #  """, web_element)


        # Press on More Info Section.
        siebel_more_info = hold.until(EC.element_to_be_clickable((By.LINK_TEXT, "More Info")))
        SD_Robot.execute_script("arguments[0].click();", siebel_more_info)
        time.sleep(2)

        # Fill Reachability.
        siebel_reachability = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='a_2']/div/table/tbody/tr[5]/td[5]/div/input")))
        SD_Robot.execute_script(f"arguments[0].value = 'SMS Sent';", siebel_reachability)
        siebel_reachability.send_keys(Keys.ENTER)
        time.sleep(0.50)

        # Fill Validity.
        siebel_validity = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='a_2']/div/table/tbody/tr[6]/td[5]/div/input")))
        SD_Robot.execute_script(f"arguments[0].value = 'Valid';", siebel_validity)
        siebel_validity.send_keys(Keys.ENTER)
        time.sleep(0.50)

        # Fill  Customer Satisfaction.
        siebel_customer_satisfaction = hold.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='a_2']/div/table/tbody/tr[10]/td[4]/div/input")))
        SD_Robot.execute_script(f"arguments[0].value = 'Satisfied / Solved';", siebel_customer_satisfaction)
        siebel_customer_satisfaction.send_keys(Keys.ENTER)
        time.sleep(0.50)

        mouse_kyb.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
        # --------------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    def send_sms():
        """Send SMS to the customer edu him/her that the action done"""
        time.sleep(3)

        # Open SMS Window.
        mouse_kyb.key_down(Keys.ALT).key_down(Keys.F9).key_up(Keys.F9).key_up(Keys.ALT).perform()
        time.sleep(4)

        # Press OK BTN.
        siebel_ok_btn = hold.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='s_S_A3_div']/form/div/div[2]/span[1]/button")))
        SD_Robot.execute_script("arguments[0].click();", siebel_ok_btn)
        time.sleep(1)

        # Fill SMS Name.
        siebel_sms_field = hold.until(EC.visibility_of_element_located((By.XPATH,
                                                                        "//*[@id='a_4']/div/table/tbody/tr[4]/td[3]/div/"
                                                                        "input[@class='siebui-ctrl-select siebui-input-popup siebui-align-left siebui-input-align-left ui-autocomplete-input']")))

        SD_Robot.execute_script(f"arguments[0].value = 'SD Move -AR';", siebel_sms_field)
        time.sleep(1)

        # Press Tab BTN to let the SMS text appear.
        mouse_kyb.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        time.sleep(1)

        # Check Mark on box of (  Send To SR Contact / Asset ) @ Bottom Right.
        siebel_box_mark = hold.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='a_4']/div/table/tbody/tr[8]/td[6]/div/input")))
        SD_Robot.execute_script("arguments[0].click();", siebel_box_mark)
        time.sleep(1)

        # Ensure the (  Send To SR Contact / Asset: ) Box is checked.
        hold.until(
            EC.element_located_to_be_selected((By.XPATH, "//*[@id='a_4']/div/table/tbody/tr[8]/td[6]/div/input")))
        time.sleep(1)

        # Press Send SMS.
        try:
            siebel_send_btn_1 = hold.until(EC.element_to_be_clickable((By.XPATH,
                                                                       "//div[@class='siebui-applet siebui-form siebui-collapsible-applet siebui-formapplet-column Selected siebui-active siebui-applet-active siebui-hilight siebui-commit-pending']"
                                                                       "/form/table/tbody/tr/td/span/span[1]/button")))
            SD_Robot.execute_script("arguments[0].click();", siebel_send_btn_1)
            time.sleep(5)


        except:
            siebel_send_btn_2 = hold.until(
                EC.element_to_be_clickable((By.XPATH, "//form/table/tbody/tr/td/span/span[1]/button")))
            SD_Robot.execute_script("arguments[0].click();", siebel_send_btn_2)
            time.sleep(5)

    # ------------------------------------------------------------------------------------------------------------------
    def close_sr():
        """Close Siebel SR."""
        time.sleep(1)

        # Siebel Status Element.
        siebel_status = hold.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='a_1']/div/table/tbody/tr[5]/td[9]/div/input")))

        SD_Robot.execute_script(f"arguments[0].value = '';", siebel_status)
        time.sleep(0.50)
        SD_Robot.execute_script(f"arguments[0].value = 'In Progress';", siebel_status)
        time.sleep(0.50)
        siebel_status.send_keys(Keys.ENTER)
        time.sleep(2)
        SD_Robot.execute_script(f"arguments[0].value = '';", siebel_status)
        time.sleep(0.50)
        SD_Robot.execute_script(f"arguments[0].value = 'Closed';", siebel_status)
        time.sleep(1)
        # --------------------------------------------------------------------------------------------------
        siebel_status_span = hold.until(EC.visibility_of_element_located((By.XPATH,
                                                                          "//*[@id='a_1']/div/table/tbody/tr[5]/td[9]/div/*[@id='s_1_1_161_0_icon']")))
        SD_Robot.execute_script("arguments[0].click();", siebel_status_span)
        time.sleep(2)
        # --------------------------------------------------------------------------------------------------

        # Fill textarea.
        siebel_textarea = hold.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='a_1']/div/table/tbody/tr[5]/td[10]/div/textarea")))
        time.sleep(0.50)
        siebel_textarea.send_keys("SD Moved By Sle")
        time.sleep(1)
        # --------------------------------------------------------------------------------------------------

        # Siebel Sub-Status Element.
        siebel_sub_status = hold.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='a_1']/div/table/tbody/tr[6]/td[7]/div/input")))
        SD_Robot.execute_script(f"arguments[0].value = ' Handled';", siebel_sub_status)
        time.sleep(1)
        siebel_sub_status.send_keys(Keys.ENTER)
        time.sleep(1.5)

        # --------------------------------------------------------------------------------------------------
        # Save Action.
        mouse_kyb.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
        # --------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------

    more_info()
    send_sms()
    close_sr()

    return f"Done 100%"



# -----------------------
# running environment.
# -----------------------

# 1- Get the SR Number from relative text file.
print("\nPlease ensure that the text file with name (SR_Source) is exist in same folder")
time.sleep(1)
input("\nClose the file if opened, Press Enter to Skip.")
time.sleep(1)

current_directory = os.getcwd()
file_path = f"{current_directory}\\SR_Source.txt"

with open(file_path , "r" , encoding="utf-8" ) as sr_list :
    contents = sr_list.read().splitlines()

# ------------------------------------------------------------------------------------

# 2- Enter Siebel username and password.
siebel_username = str(input("\nEnter Siebel username, Press Enter: "))

print("\nSubmit Siebel Password in the external window, then close it.")

# Global variable to store the password siebel.
siebel_password = ""

def get_password_siebel():
    global siebel_password
    siebel_password = siebel_password_entry.get()

siebel_root = tk.Tk()
siebel_root.title("Password Input")

tk.Label(siebel_root, text="Enter siebel password:").pack()

# Entry widget with masked input
siebel_password_entry = tk.Entry(siebel_root, show="*")
siebel_password_entry.pack()

# Submit button
tk.Button(siebel_root, text="Submit", command=get_password_siebel).pack()

siebel_root.mainloop()

print(f"\nsiebel password : {'*' * len(siebel_password)}")
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

# 3- Enter AX username and password.
ax_username = str(input("\nEnter AX username, Press Enter : "))

print("\nSubmit AX Password in the external window, then close it.")

# Global variable to store the password AX.
ax_password = ""

def get_password_ax():
    global ax_password
    ax_password = ax_password_entry.get()

ax_root = tk.Tk()
ax_root.title("Password Input")

tk.Label(ax_root, text="Enter AX password:").pack()

# Entry widget with masked input
ax_password_entry = tk.Entry(ax_root, show="*")
ax_password_entry.pack()

# Submit button
tk.Button(ax_root, text="Submit", command=get_password_ax).pack()

ax_root.mainloop()

print(f"\nAX password : {'*' * len(ax_password)}")

# ------------------------------------------------------------------------------------
print(f"\nRunning Module.")
# ------------------------------------------------------------------------------------

# 4- Call FXs of siebel_login and ax_login.
siebel_login(siebel_username,siebel_password)
ax_login(ax_username,ax_password)
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# 5- Start the SR full cycle.
for each_sr in contents :
    sr_start_time = time.time()

    try:
        function_calling = full_ticket_cycle(each_sr)
        print(f"""
\n----------------------------------------------------------
SR # {each_sr}
SR Duration : {str(time.time() - sr_start_time)[:3]} Sec
SR Feedback : {function_calling}
------------------------------------------------------------\n""")
        time.sleep(1)
        # Press Service Request To Exit.
        hold.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s_sctrl_tabScreen']/ul/li[8]"))).click()
        time.sleep(1)

    except Exception as e :
        # Take screenshot to validate the error reason.
        SD_Robot.save_screenshot(f"Error Of SR Number {str(each_sr)}.png")

        # print the impacted SR.
        print("-" * 95)
        print(f"SR Number {each_sr}, impacted with below Error, please check it manually.")
        print("-" * 80)
        print(f"Error Type : {e}")
        print("-" * 95)
        #---------------------------------------------------------------------------------------------
        def current_location() :
            """Get the current location"""
            current_tab = SD_Robot.current_window_handle
            tab_index = SD_Robot.window_handles.index(current_tab)

            if tab_index == 0 :
                return "Siebel"

            elif tab_index == 1 :
                return "AX"
        #------------------------------------
        #------------------------------------

        if current_location() == "Siebel" :
            siebel_login(siebel_username, siebel_password)
            time.sleep(0.25)
            SD_Robot.switch_to.window(AX_tab)
            time.sleep(0.25)
            SD_Robot.close()
            time.sleep(0.25)
            SD_Robot.switch_to.window(Siebel_tab)
            time.sleep(0.25)
            ax_login(ax_username, ax_password)
            time.sleep(0.25)
            SD_Robot.switch_to.window(Siebel_tab)
        #-----------------------------------------------------------

        if current_location() == "AX" :
            time.sleep(0.25)
            SD_Robot.close()
            time.sleep(0.25)
            SD_Robot.switch_to.window(Siebel_tab)
            time.sleep(0.25)
            siebel_login(siebel_username, siebel_password)
            time.sleep(0.25)
            ax_login(ax_username, ax_password)
            time.sleep(0.25)
            SD_Robot.switch_to.window(Siebel_tab)


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
print(f"\nFull Time of APP : {round(time.time() - app_start_time, 2)} Sec\n")
time.sleep(2)
print("Exiting...")
time.sleep(3)
SD_Robot.quit()
time.sleep(2)
input("Press Enter To Exit")
print("Browser closed. Application finished.")
# -----------------------------------------------------------------------
