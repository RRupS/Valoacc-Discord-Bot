# Imports
import discord, sqlite3, random, os
from discord.ext import commands
from discord.errors import Forbidden

# Database Connection
con = sqlite3.connect('valoacc.db')
cur = con.cursor()

# Get Token
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

############################################
#                                          #
#                 SETTINGS                 #
#                                          #
############################################

VERSION = '0.1'
AUTHOR = 'rups#0343'
OWNERS_ID = [299232190078648323,]
AUTHORITIES_ID = [
    299232190078648323, #Yusuf
    328150462865866753, #Haktan
    409333483597594624, #Enes
    800454344344338484, #Yiğit
    321025814982426624  #Salih
]
EMOTES = {
    'kredi': '<:Kredi:864260738792292382>',
    'vp': '<:ValoaccVP:865183881283502101>',
    'radiant': '<:ValoaccRadiant:864266868528119848>',
    'immortal': '<:ValoaccImmortal:864266842331676712>',
    'diamond': '<:ValoaccDiamond:864266813637525515>',
    'platinum': '<:ValoaccPlatinum:864266784282247168>',
    'gold': '<:ValoaccGold:864266756624220173>',
    'silver': '<:ValoaccSilver:864266733430374441>',
    'bronze': '<:ValoaccBronze:864266709942796298>',
    'iron': '<:ValoaccIron:864266672461185055>',
    'unranked': '<:ValoaccUnranked:865477194554015775>'
}
ACC_PRICE_LIST = {
    'derecesiz': 12,
    'demir': 7,
    'bronz': 10,
    'gumus': 15,
    'altin': 22,
    'plat': 35,
    'elmas': 70,
    'olumsuzluk': 110,
    'radyant': 999
}
VP_PRICE_LIST = {
    '300': 15,
    '600': 25,
    '1250': 45,
    '2500': 90,
    '4400': 155,
    '8400': 305
}

############################################
#                                          #
#                 ACTIONS                  #
#                                          #
############################################

async def send_embed(channel, embed):
    try:
        await channel.send(embed=embed)
    except Forbidden:
        await channel.send("Bu kanala embed mesaj gönderilemiyor. Lütfen izinleri kontrol edin.")

############################################
#                                          #
#                  CREDIT                  #
#                                          #
############################################

def add_credit(user, quantity):
    cur.execute("SELECT * FROM discord_users WHERE id = {}".format(user.id))
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO discord_users VALUES ({}, {})".format(user.id, int(quantity)))
        con.commit()
    else:
        cur.execute("SELECT * FROM discord_users WHERE id = {}".format(user.id))
        userr = cur.fetchall()
        userr_credit = userr[0][1]
        userr_credit += int(quantity)
        cur.execute('UPDATE discord_users SET credit = {} WHERE id = {}'.format(userr_credit, user.id))
        con.commit()

def reset_credit(user):
    cur.execute("UPDATE discord_users SET credit = 0 WHERE id = {}".format(user.id))
    con.commit()

def get_credit(user):
    cur.execute("SELECT * FROM discord_users WHERE id = {}".format(user.id))
    userr = cur.fetchall()
    if len(userr) == 0:
        return 0
    else:
        return userr[0][1]

############################################
#                                          #
#                  STOCK                   #
#                                          #
############################################

async def add_acc_stock(username, password, rank, guild, message_author):
    cur.execute("SELECT * FROM accounts WHERE username = '{}'".format(username))
    if len(cur.fetchall()) != 0:
        return 0
    else:
        acc_id = random.randint(100000, 999999)
        cur.execute("INSERT INTO accounts VALUES ('{}', '{}', '{}', '{}')".format(acc_id, username, password, rank))
        con.commit()
        embed = discord.Embed(title='Valoacc Log Sistemi', description='Stoğa bir ürün eklendi.', color=0x33ff00)
        embed.add_field(name='ID', value=acc_id, inline=False)
        embed.add_field(name='Kullanıcı Adı', value=username, inline=False)
        embed.add_field(name='Şifre', value=password, inline=False)
        embed.add_field(name='Rütbe', value=rank, inline=False)
        embed.add_field(name='Yetkili', value=message_author.mention, inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/801490295924588585/864936680947187782/valorantlogo.png')
        embed.set_footer(text="Valoacc ● dev. by rups")
        stock_log_channel = guild.get_channel(864261324720701440)
        await send_embed(stock_log_channel, embed)
        return acc_id

async def del_acc_stock(idd, guild, message_author):
    cur.execute("SELECT * FROM accounts WHERE id = '{}'".format(idd))
    del_acc = cur.fetchall()
    if len(del_acc) == 1:
        cur.execute("DELETE FROM accounts WHERE id = '{}'".format(idd))
        con.commit()
        embed = discord.Embed(title='Valoacc Log Sistemi', description='Stoktan bir ürün eksildi.', color=0xff0000)
        embed.add_field(name='ID', value=del_acc[0][0], inline=False)
        embed.add_field(name='Kullanıcı Adı', value=del_acc[0][1], inline=False)
        embed.add_field(name='Şifre', value=del_acc[0][2], inline=False)
        embed.add_field(name='Rütbe', value=del_acc[0][3], inline=False)
        embed.add_field(name='Yetkili', value=message_author.mention, inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/801490295924588585/864936680947187782/valorantlogo.png')
        embed.set_footer(text="Valoacc ● dev. by rups")
        stock_log_channel = guild.get_channel(864261324720701440)
        await send_embed(stock_log_channel, embed)
        return 'Hesap başarıyla stoktan silindi.'
    else:
        return 'Belirtmiş olduğunuz ID\'ye sahip bir hesap bulunamadı.'

async def add_vp_stock(code, quantity, guild, message_author):
    cur.execute("SELECT * FROM valorant_points WHERE code = '{}'".format(code))
    if len(cur.fetchall()) != 0:
        return 'Bu e-pin kodu stokta mevcut.'
    else:
        cur.execute("INSERT INTO valorant_points VALUES ('{}', '{}')".format(code, quantity))
        con.commit()
        embed = discord.Embed(title='Valoacc Log Sistemi', description='Stoğa bir ürün eklendi.', color=0x33ff00)
        embed.add_field(name='E-Pin Kodu', value=code, inline=False)
        embed.add_field(name='Miktar', value=quantity, inline=False)
        embed.add_field(name='Yetkili', value=message_author.mention, inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/801490295924588585/864936680947187782/valorantlogo.png')
        embed.set_footer(text="Valoacc ● dev. by rups")
        stock_log_channel = guild.get_channel(864261324720701440)
        await send_embed(stock_log_channel, embed)
        return 'Valorant puanınız başarıyla stoğa eklenmiştir.'

async def del_vp_stock(code, guild, message_author):
    cur.execute("SELECT * FROM valorant_points WHERE code = '{}'".format(code))
    del_code = cur.fetchall()
    if len(del_code) == 0:
        return 'Belirtmiş olduğunuz e-pin kodu stokta bulunamadı.'
    else:
        cur.execute("DELETE FROM valorant_points WHERE code = '{}'".format(code))
        con.commit()
        embed = discord.Embed(title='Valoacc Log Sistemi', description='Stoktan bir ürün eksildi.', color=0xff0000)
        embed.add_field(name='E-Pin Kodu', value=del_code[0][0], inline=False)
        embed.add_field(name='Miktar', value=del_code[0][1], inline=False)
        embed.add_field(name='Yetkili', value=message_author.mention, inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/801490295924588585/864936680947187782/valorantlogo.png')
        embed.set_footer(text="Valoacc ● dev. by rups")
        stock_log_channel = guild.get_channel(864261324720701440)
        await send_embed(stock_log_channel, embed)
        return 'Kod başarıyla stoktan silindi.'