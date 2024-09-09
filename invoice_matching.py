import requests
import pandas as pd
from bs4 import BeautifulSoup


def fetch_html_content(url):
    """從指定URL獲取HTML內容。"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None


def check_jackpot(number, jackpot_numbers):
    """根據輸入號碼比對中獎結果。"""
    prize = "銘謝惠顧!"

    for jackpot_number in jackpot_numbers:
        if number == jackpot_number:
            prize = "恭喜! 對中頭獎 20 萬元！"
            break
        elif number[-7:] == jackpot_number[-7:]:
            prize = "恭喜! 對中二獎 4 萬元！"
            break
        elif number[-6:] == jackpot_number[-6:]:
            prize = "恭喜! 對中三獎 1 萬元！"
            break
        elif number[-5:] == jackpot_number[-5:]:
            prize = "恭喜! 對中四獎 4 千元！"
            break
        elif number[-4:] == jackpot_number[-4:]:
            prize = "恭喜! 對中五獎 1 千元！"
            break
        elif number[-3:] == jackpot_number[-3:]:
            prize = "恭喜! 對中六獎 2 百元！"
            break

    print(prize)


def parse_jackpot_numbers(soup):
    """解析網頁中的中獎號碼。"""
    special_award_number = soup.find_all('span', class_="font-weight-bold etw-color-red")[0].text
    special_prize_number = soup.find_all('span', class_="font-weight-bold etw-color-red")[1].text

    jackpot_red_numbers = soup.find_all('span', class_="font-weight-bold etw-color-red")[2:5]
    jackpot_all_numbers = soup.find_all('span', class_="font-weight-bold")

    jackpot_black_numbers = [jackpot_all_numbers[i].text for i in [2, 4, 6]]

    first_jackpot_number = jackpot_black_numbers[0] + jackpot_red_numbers[0].text
    second_jackpot_number = jackpot_black_numbers[1] + jackpot_red_numbers[1].text
    third_jackpot_number = jackpot_black_numbers[2] + jackpot_red_numbers[2].text

    jackpot_numbers = [first_jackpot_number, second_jackpot_number, third_jackpot_number]

    return special_award_number, special_prize_number, jackpot_numbers


def main():
    url = "https://invoice.etax.nat.gov.tw/index.html"
    html_content = fetch_html_content(url)

    if html_content is None:
        return

    soup = BeautifulSoup(html_content, "html.parser")
    special_award_number, special_prize_number, jackpot_numbers = parse_jackpot_numbers(soup)
    t = 1
    while t:
        invoice_number = input('請輸入你的發票號碼：')

        if invoice_number == special_award_number:
            print("恭喜! 對中特別獎 1000 萬元！")
        elif invoice_number == special_prize_number:
            print("恭喜! 對中特獎 200 萬元！")
        else:
            check_jackpot(invoice_number, jackpot_numbers)
        yes_no = input("還有發票要對嗎(有/沒有):")
        if yes_no == "有":
            t = 1
        elif yes_no == "沒有":
            t = 0


if __name__ == "__main__":
    main()
