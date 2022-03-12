import discord, utils, sqlite3
from discord.ext import commands

# Database Connection
con = sqlite3.connect('valoacc.db')
cur = con.cursor()

class Genel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kredim(self, ctx):
        credit = utils.get_credit(ctx.message.author)
        await ctx.send('<@{}> kullanıcısının kredisi: {} **{}**'.format(ctx.message.author.id, utils.EMOTES['kredi'], credit))

    
    @commands.command()
    async def satinal(self, ctx, result_id=None):
        if result_id != None:
            if result_id in utils.ACC_PRICE_LIST.keys() or result_id in utils.VP_PRICE_LIST.keys():
                cur.execute("SELECT * FROM accounts WHERE rank = '{}'".format(result_id))
                acc_count = len(cur.fetchall())
                cur.execute("SELECT * FROM valorant_points WHERE quantity = '{}'".format(result_id))
                vp_count = len(cur.fetchall())
                cur.execute("SELECT * FROM discord_users WHERE id = {}".format(ctx.message.author.id))
                if len(cur.fetchall()) == 0:
                    user_money = 0
                else:
                    cur.execute("SELECT * FROM discord_users WHERE id = {}".format(ctx.message.author.id))
                    user_money = cur.fetchall()[0][1]
                if acc_count > 0 or vp_count > 0:
                    if acc_count > 0:
                        price = utils.ACC_PRICE_LIST[result_id]
                        if user_money >= price:
                            cur.execute("SELECT * FROM accounts WHERE rank = '{}'".format(result_id))
                            account = cur.fetchall()[0]
                            utils.add_credit(ctx.message.author, -price)
                            await utils.del_acc_stock(account[0], ctx.message.guild, ctx.message.author)
                            await ctx.message.author.send('Satın alımınız başarı ile tamamlanmıştır.\n\n**__ÜRÜN BİLGİLERİ__**\n**Kullanıcı Adı:** {}\n**Şifre:** {}\n**Rütbe:** {}'.format(account[1], account[2], account[3]))
                            embed = discord.Embed(title='Valoacc Log Sistemi', description='Bir ürün satın alındı.', color=0xffa400)
                            embed.add_field(name='Ürün ID', value=result_id, inline=False)
                            embed.add_field(name='Fiyat', value=price, inline=False)
                            embed.add_field(name='Müşteri', value=ctx.message.author.mention, inline=False)
                            embed.set_footer(text="Valoacc ● dev. by rups")
                            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/801490295924588585/864936680947187782/valorantlogo.png')
                            market_log_channel = self.bot.get_channel(864261575488700427)
                            await utils.send_embed(market_log_channel, embed)
                        else:
                            await ctx.send('`{}` ID\'sine sahip ürünü almak için yeterli krediniz bulunmuyor.'.format(result_id))
                    elif vp_count > 0:
                        price = utils.VP_PRICE_LIST[result_id]
                        if user_money >= price:
                            cur.execute("SELECT * FROM valorant_points WHERE quantity = '{}'".format(result_id))
                            vp_code = cur.fetchall()[0]
                            utils.add_credit(ctx.message.author, -price)
                            await utils.del_vp_stock(vp_code[0], ctx.message.guild, ctx.message.author)
                            await ctx.message.author.send('Satın alımınız başarı ile tamamlanmıştır.\n\n**__ÜRÜN BİLGİLERİ__**\n**E-Pin Kodu:** {}\n**Miktar:** {}'.format(vp_code[0], vp_code[1]))
                            embed = discord.Embed(title='Valoacc Log Sistemi', description='Bir ürün satın alındı.', color=0xffa400)
                            embed.add_field(name='E-Pin Kodu', value=vp_code[0], inline=False)
                            embed.add_field(name='Miktar', value=vp_code[1], inline=False)
                            embed.add_field(name='Fiyat', value=price, inline=False)
                            embed.add_field(name='Müşteri', value=ctx.message.author.mention, inline=False)
                            embed.set_footer(text="Valoacc ● dev. by rups")
                            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/801490295924588585/864936680947187782/valorantlogo.png')
                            market_log_channel = self.bot.get_channel(864261575488700427)
                            await utils.send_embed(market_log_channel, embed)
                        else:
                            await ctx.send('`{}` ID\'sine sahip ürünü almak için yeterli krediniz bulunmuyor.'.format(result_id))
                else:
                    await ctx.send('Almak istediğiniz ürün stoklarda bulunmuyor.')
            else:
                await ctx.send('`{}` ID\'sine sahip bir ürün bulunamadı.'.format(result_id))
        else:
            await ctx.send('Satın almak istediğiniz ürünün **Ürün ID**\'sini girmelisiniz.')

def setup(bot):
    bot.add_cog(Genel(bot))