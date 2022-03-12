import discord, utils
from discord.ext import commands

class Yetkili(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def kredi(self, ctx, arg=None, user:discord.Member=None, quantity=None):
        """Kredi ekleme/silme/görüntüleme."""
        if ctx.message.author.id in utils.OWNERS_ID:
            if arg != None:
                if arg == 'ekle':
                    if user != None:
                        if quantity != None:
                            if quantity.isdigit():
                                utils.add_credit(user, quantity)
                                await ctx.send('<@{}> kullanıcısına {} **{}** kredi eklendi.'.format(user.id, utils.EMOTES['kredi'], quantity))
                            else:
                                await ctx.send('Geçerli bir miktar girmelisiniz.')
                        else:
                            await ctx.send('Geçerli bir miktar girmelisiniz.')
                    else:
                        await ctx.send('Geçerli bir kullanıcı etiketlemelisiniz.')
                elif arg == 'sifirla':
                    if user != None:
                        utils.reset_credit(user)
                        await ctx.send('<@{}> isimli kullanıcının kredisi başarıyla sıfırlandı.'.format(user.id))
                    else:
                        await ctx.send('Geçerli bir kullanıcı etiketlemelisiniz.')
                elif arg == 'sorgula':
                    if user != None:
                        credit = utils.get_credit(user)
                        await ctx.send('<@{}> kullanıcısının kredisi: {} **{}**'.format(user.id, utils.EMOTES['kredi'], credit))
                    else:
                        await ctx.send('Bir kullanıcı etiketlemelisiniz.')
                else:
                    await ctx.send('Geçerli bir argüman belirtmelisiniz. [`ekle`, `sifirla`, `sorgula`]')
            else:
                await ctx.send('Geçerli bir argüman belirtmelisiniz. [`ekle`, `sifirla`, `sorgula`]')
    
    @kredi.error
    async def kredi_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Geçerli bir kullanıcı etiketlemelisiniz.')
        else:
            print(error)


    @commands.command()
    async def stok(self, ctx, *args):
        if ctx.message.author.id in utils.AUTHORITIES_ID:
            if 'ekle' in args:
                await ctx.send('Stoğa eklemek istediğiniz hesabın kullanıcı adı nedir?\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                acc_username = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                await ctx.send('Stoğa eklemek istediğiniz hesabın şifresi nedir?\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                acc_password = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                await ctx.send('Stoğa eklemek istediğiniz hesabın rankı nedir?\nSeçenekler: `derecesiz`, `demir`, `bronz`, `gumus`, `altin`, `plat`, `elmas`, `olumsuzluk`\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                acc_rank = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                if acc_rank.content in utils.ACC_PRICE_LIST.keys() and acc_rank.content != 'radyant':
                    acc_id = await utils.add_acc_stock(acc_username.content, acc_password.content, acc_rank.content, ctx.message.guild, ctx.message.author)
                    if acc_id == 0: await ctx.send('Bu kullanıcı adına sahip bir hesap stokta mevcut.')
                    else: await ctx.send('Hesabınız başarıyla stoğa eklenmiştir.\n**ID:** {}'.format(acc_id))
                else:
                    await ctx.send('Geçerli bir rank girmelisiniz.')
            elif 'sil' in args:
                await ctx.send('Stoktan silmek istediğiniz hesabın ID\'si nedir?\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                del_id = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                reply = await utils.del_acc_stock(del_id.content, ctx.message.guild, ctx.message.author)
                await ctx.send(reply)
            else:
                await ctx.send('Geçerli bir argüman belirtmelisiniz. [`ekle`, `sil`]')
        else:
            await ctx.send('Bu komutunu kullanmak için gerekli izne sahip değilsiniz.')


    @commands.command()
    async def vpstok(self, ctx, *args):
        if ctx.message.author.id in utils.AUTHORITIES_ID:
            if 'ekle' in args:
                await ctx.send('Stoğa eklemek istediğiniz valorant puanının miktarı nedir?\nSeçenekler: `300`, `600`, `1250`, `2500`, `4400`, `8400`\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                quantity = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                await ctx.send('Stoğa eklemek istediğiniz e-pin kodunu girin.\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                code = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                if quantity.content in utils.VP_PRICE_LIST.keys():
                    reply = await utils.add_vp_stock(code.content, quantity.content, ctx.message.guild, ctx.message.author)
                    await ctx.send(reply)
                else:
                    await ctx.send('Geçerli bir miktar girmelisiniz.')
            elif 'sil' in args:
                await ctx.send('Stoktan silmek istediğiniz e-pin kodu nedir?\n\n`Cevap vermemeniz durumunda işlem 60 saniye içerisinde iptal edilecektir.`')
                del_code = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                reply = await utils.del_vp_stock(del_code.content, ctx.message.guild, ctx.message.author)
                await ctx.send(reply)
            else:
                await ctx.send('Geçerli bir argüman belirtmelisiniz. [`ekle`, `sil`]')
        else:
            await ctx.send('Bu komutunu kullanmak için gerekli izne sahip değilsiniz.')

def setup(bot):
    bot.add_cog(Yetkili(bot))