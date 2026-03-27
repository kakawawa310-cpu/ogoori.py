import discord
from discord import app_commands
import os
from flask import Flask
from threading import Thread

class MyClient(discord.Client):
    def __init__(self):
        # メンバー情報取得などの権限をすべて有効にする
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # スラッシュコマンドを同期
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f'ログイン成功: {client.user}')

# --- スラッシュコマンド：番号割り当て ---
@client.tree.command(name="assign", description="ユーザーに番号を割り当てて保存します")
@app_commands.describe(member="対象のユーザー", num="1〜50の番号")
async def assign(interaction: discord.Interaction, member: discord.Member, num: int):
    if not (1 <= num <= 50):
        await interaction.response.send_message("1から50の間の番号を入力してください。", ephemeral=True)
        return

    try:
        # data.txtに保存（Renderでは再起動すると消える点に注意）
        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(f"ユーザー: {member.display_name}, 割り当て番号: {num}\n")
        
        await interaction.response.send_message(f"{member.mention} さんに番号 {num} を割り当て、保存しました！")
    except Exception as e:
        await interaction.response.send_message(f"保存中にエラーが発生しました: {e}", ephemeral=True)

# --- スラッシュコマンド：挨拶 ---
@client.tree.command(name="hello", description="挨拶をします")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention}さん、こんにちは！")

# Webサーバーを起動
keep_alive()

# Botを起動
client.run(os.getenv('MTQ3NjkxMDk4NDI4MjI0MzEyNA.GND0YU.MS8P4XZQwGSoZEI9Tbe2GZd3QHLuNlwJfi_45k'))

