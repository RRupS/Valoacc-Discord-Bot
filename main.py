import discord, os, utils, sqlite3
from discord.ext import commands, tasks

Bot = commands.Bot(command_prefix='!')

# Database Connection
con = sqlite3.connect('valoacc.db')
cur = con.cursor()

############################################
#                                          #
#                  EVENTS                  #
#                                          #
############################################

@tasks.loop(minutes=1)
async def stock_update():
    unranked_acc_count = iron_acc_count = bronze_acc_count = silver_acc_count = gold_acc_count = plat_acc_count = diamond_acc_count = immortal_acc_count = 0
    cur.execute("SELECT * FROM accounts WHERE rank = 'derecesiz'")
    unranked_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'demir'")
    iron_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'bronz'")
    bronze_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'gumus'")
    silver_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'altin'")
    gold_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'plat'")
    plat_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'elmas'")
    diamond_acc_count = len(cur.fetchall())
    cur.execute("SELECT * FROM accounts WHERE rank = 'olumsuzluk'")
    immortal_acc_count = len(cur.fetchall())
    embed=discord.Embed(title="Valorant TR Hesaplar", description="● Hesap satın almanız durumunda hesap otomatik olarak teslim edilmektedir.\n● Hesap satın almak için <@864195945359736883> DM kutusu üzerinden `!satın-al <ÜrünID>` komutunu kullanabilirsiniz.\n● Hesapların mail adresleri onaylanmamıştır, satın aldıktan sonra **playvalorant.com** adresi üzerinden mail adresinizi ekleyip onaylatabilirsiniz.\n\n**NOT**: Stok bilgileri 1 dakikada bir yenilenmektedir.", color=0xffa400)
    embed.add_field(name="<:ValoaccUnranked:865477194554015775> Derecesiz Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `derecesiz`".format(utils.ACC_PRICE_LIST['derecesiz'], unranked_acc_count), inline=True)
    embed.add_field(name="<:ValoaccIron:864266672461185055> Demir Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `demir`".format(utils.ACC_PRICE_LIST['demir'], iron_acc_count), inline=True)
    embed.add_field(name="<:ValoaccBronze:864266709942796298> Bronz Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `bronz`".format(utils.ACC_PRICE_LIST['bronz'], bronze_acc_count), inline=True)
    embed.add_field(name="<:ValoaccSilver:864266733430374441> Gümüş Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `gumus`".format(utils.ACC_PRICE_LIST['gumus'], silver_acc_count), inline=True)
    embed.add_field(name="<:ValoaccGold:864266756624220173> Altın Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `altin`".format(utils.ACC_PRICE_LIST['altin'], gold_acc_count), inline=True)
    embed.add_field(name="<:ValoaccPlat:864266784282247168> Platin Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `plat`".format(utils.ACC_PRICE_LIST['plat'], plat_acc_count), inline=True)
    embed.add_field(name="<:ValoaccDiamond:864266813637525515> Elmas Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `elmas`".format(utils.ACC_PRICE_LIST['elmas'], diamond_acc_count), inline=True)
    embed.add_field(name="<:ValoaccImmortal:864266842331676712> Ölümsüzlük Hesap", value="Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `olumsuzluk`".format(utils.ACC_PRICE_LIST['olumsuzluk'], immortal_acc_count), inline=True)
    embed.add_field(name="<:ValoaccRadiant:864266868528119848> Radyant Hesap", value="Satılmamaktadır.", inline=True)
    embed.set_footer(text="Valoacc ● dev. by rups")
    msg = await Bot.get_channel(864255714436710440).fetch_message(864574198008381460)
    await msg.edit(embed=embed)

@tasks.loop(minutes=1)
async def stock_update_vp():
    vp_300_count = vp_600_count = vp_1250_count = vp_2500_count = vp_4400_count = vp_8400_count = 0
    cur.execute("SELECT * FROM valorant_points WHERE quantity = '300'")
    vp_300_count = len(cur.fetchall())
    cur.execute("SELECT * FROM valorant_points WHERE quantity = '600'")
    vp_600_count = len(cur.fetchall())
    cur.execute("SELECT * FROM valorant_points WHERE quantity = '1250'")
    vp_1250_count = len(cur.fetchall())
    cur.execute("SELECT * FROM valorant_points WHERE quantity = '2500'")
    vp_2500_count = len(cur.fetchall())
    cur.execute("SELECT * FROM valorant_points WHERE quantity = '4400'")
    vp_4400_count = len(cur.fetchall())
    cur.execute("SELECT * FROM valorant_points WHERE quantity = '8400'")
    vp_8400_count = len(cur.fetchall())
    embed = discord.Embed(title='Valorant Puanları', description='● Valorant puanı satın almanız durumunda e-pin kodu otomatik olarak teslim edilmektedir.\n● Valorant puanı satın almak için <@864195945359736883> DM kutusu üzerinden `!satın-al <ÜrünID>` komutunu kullanabilirsiniz.\n\n**NOT**: Stok bilgileri 1 dakikada bir yenilenmektedir.', color=0xffa400)
    embed.add_field(name='<:ValoaccVP:865183881283502101> 300 Valorant Puanı', value='Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `300`'.format(utils.VP_PRICE_LIST['300'], vp_300_count), inline=True)
    embed.add_field(name='<:ValoaccVP:865183881283502101> 600 Valorant Puanı', value='Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `600`'.format(utils.VP_PRICE_LIST['600'], vp_600_count), inline=True)
    embed.add_field(name='<:ValoaccVP:865183881283502101> 1.250 Valorant Puanı', value='Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `1250`'.format(utils.VP_PRICE_LIST['1250'], vp_1250_count), inline=True)
    embed.add_field(name='<:ValoaccVP:865183881283502101> 2.500 Valorant Puanı', value='Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `2500`'.format(utils.VP_PRICE_LIST['2500'], vp_2500_count), inline=True)
    embed.add_field(name='<:ValoaccVP:865183881283502101> 4.400 Valorant Puanı', value='Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `4400`'.format(utils.VP_PRICE_LIST['4400'], vp_4400_count), inline=True)
    embed.add_field(name='<:ValoaccVP:865183881283502101> 8.400 Valorant Puanı', value='Fiyat: <:Kredi:864260738792292382> {}\nStok: {}\nÜrün ID: `8400`'.format(utils.VP_PRICE_LIST['8400'], vp_8400_count), inline=True)
    embed.set_footer(text='Valoacc ● dev. by rups')
    msg = await Bot.get_channel(863797923749691463).fetch_message(865174974288101386)
    await msg.edit(embed=embed)

@Bot.event
async def on_ready():
    print('Valoacc is activated!')
    await Bot.change_presence(status=discord.Status.idle)
    stock_update.start()
    stock_update_vp.start()

############################################
#                                          #
#                   COGS                   #
#                                          #
############################################

@Bot.command()
async def load(ctx, extension):
    Bot.load_extension(f'cogs.{extension}')

@Bot.command()
async def unload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')

@Bot.command()
async def reload(ctx, extension):
    Bot.unload_extension(f'cogs.{extension}')
    Bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'): Bot.load_extension(f'cogs.{filename[:-3]}')

Bot.run(utils.TOKEN)