#!/usr/bin/env python3
"""
神戸パンダBot - タンタンがいなくなってからの日数をカウント
2025年6月25日を1日目として、X（Twitter）に投稿します
"""

import os
from datetime import datetime, timezone, timedelta
import tweepy
from dotenv import load_dotenv

load_dotenv()

START_DATE = datetime(2025, 6, 25, tzinfo=timezone.utc)


def calculate_days_since_start():
    """2025年6月25日からの経過日数を計算"""
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst)
    today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    start_date_jst = START_DATE.astimezone(jst).replace(hour=0,
                                                        minute=0,
                                                        second=0,
                                                        microsecond=0)

    days_passed = (today_midnight - start_date_jst).days + 1

    return days_passed


def create_message(days):
    """投稿メッセージを作成"""
    return f"神戸にパンダがいなくなってから、{days}日目です。"


def post_to_twitter(message):
    """X（Twitter）に投稿"""
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError(
           
        )

    client = tweepy.Client(consumer_key=api_key,
                           consumer_secret=api_secret,
                           access_token=access_token,
                           access_token_secret=access_token_secret)

    response = client.create_tweet(text=message)
    return response


def main():
    """メイン処理"""
    try:
        days = calculate_days_since_start()
        print(f"経過日数: {days}日")

        message = create_message(days)
        print(f"投稿メッセージ: {message}")

        response = post_to_twitter(message)
        try:
            tweet_id = response.data.get('id', '不明')
            print(f"✅ 投稿成功！ Tweet ID: {tweet_id}")
        except (AttributeError, TypeError):
            print(f"✅ 投稿成功！")

    except ValueError as e:
        print(f"❌ エラー: {e}")
        return 1
    except Exception as e:
        print(f"❌ 投稿失敗: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
