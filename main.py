# import asyncio
# import time
import discord
from apscheduler.schedulers.background import BackgroundScheduler
from user import signup, findid, edtlvl, edtmny, rstdat, rdinf, csnorst, csnonum, calbotlvl, csnokin, csnokined, \
    mazinkin, mazinkined, macnted, mazinki, mazinkied, cascnt, rank, dataget, datasave, battlew, battler, battlee, \
    getname, savesuko, readsuko, savejanken, readjanken
from dice import enchnt, csno, vsbt, batdice, dihyaku, bac, roll, setdeck, calwin
from discord.ext import commands
from math import ceil
from sudoku import sudoku_ans_set, sudoku_prt_str, make_problem, chk_sudoku, sudoku_create
import os

def dtsv_bot():
    datasave()
    sched.pause()

# token = os.environ['token']
token = open("token.txt", "r").readline()
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)  # 접두사를 $로 지정
sched = BackgroundScheduler()
sched.start()
sched.add_job(dtsv_bot, 'interval', seconds=5, id="base")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

"""
# @bot.event
# async def on_message(message):
#     if message.content.startswith('!역할분배'):
#         msgking = await message.channel.send("ゲームお誘いとかに@everyoneを使うのは迷惑かけるのかなと分けようかと思います。"
#                                          "\nお誘いのメンションを貰っても良いって方は⭕を押してください"
#                                          "\nメンションに巻き込むのがいやな方は❌を押してください"
#                                          "\nこれからは大事な告知以外は全部@活動部員でメンション致します。"
#                                          "\n何時でもここでリアクション押すと自動に切り替わるので気楽に選択してください")
#         await msgking.add_reaction("⭕")
#         await msgking.add_reaction("❌")
#         ruleIDw(msgking.id)
#     await bot.process_commands(message)


#@bot.event
# async def on_raw_reaction_add(payload):
#     msg_id = payload.message_id
#     if msg_id != 1018431463902941304:
#         return None
#     guild_id = payload.guild_id
#     user_id = payload.user_id
#     role_id = 881713001529483414
#     channel_id = payload.channel_id
#     guild = bot.get_guild(guild_id)
#     channel = bot.get_channel(channel_id)
#     msg = await channel.fetch_message(msg_id)
#     role = guild.get_role(role_id)
#     user = await guild.fetch_member(user_id)
#     if str(payload.emoji.name) == "⭕":
#         await user.add_roles(role)
#     elif str(payload.emoji.name) == "❌":
#         await user.remove_roles(role)
#     await msg.remove_reaction(payload.emoji, user)
#     await bot.process_commands(msg)
"""

@bot.command(aliases=['sdk', '数独'])
async def sudoku_play(ctx, Mxn=0):
    #문제 난이도 MxN 최대 삭제수
    MxN = int(Mxn)
    row = findid(ctx.author.id)
    if row is not None:
        sdk_tb, sdk_prize = readsuko(row)
        if sdk_prize == '0':
            money, level, cnt, ccnt = rdinf(row)
            if MxN == 0:
                sdk_str = "空欄の数が０です、入れ忘れてません？"
            elif money < 1000:
                sdk_str = "お金が足りません、一回プレイに1000円です"
            else:
                edtmny(row, money-1000)
                sdk_rw = sudoku_create()
                sdk_tb, deln = make_problem(sdk_rw, MxN)
                sdk_prize = (deln//2) * 100
                savesuko(row, sdk_tb, sdk_prize)
                sdk_tb, sdk_prize = readsuko(row)
                sdk_str = f"数独プレイに1000円使いました\n所持金 : {money}円 -> {money-1000}円"
                sched.resume()
        else:
            sdk_str = sudoku_prt_str(sdk_tb, sdk_prize, ctx.author.name)
        await ctx.send(sdk_str)
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))

@bot.command(aliases=['r', 'ダイス'])
async def dice_roll(ctx, dice):
    dice = dice.lower()
    dice_inf = dice.split('d')
    if len(dice_inf) == 2:
        try:
            dice_ko = int(dice_inf[0])
            dice_men = int(dice_inf[1])
            dice_result = roll(dice_ko, dice_men)
            dice_sum = sum(dice_result)
            mas = str(dice_sum)
            if dice_ko != 1:
                mas += " ("
                for i in range(len(dice_result)-1):
                    mas += str(dice_result[i])+"+"
                mas += str(dice_result[len(dice_result)-1]) + ")"
            await ctx.send(f"{ctx.author.mention}の{dice}ダイス結果 : {mas}")
        except:
            await ctx.send("個数や面数がおかしい！")
    else:
        await ctx.send("個数D面数でお願いします")

    
@bot.command(aliases=['w', '書く'])
async def sudoku_set(ctx, cord, ans):
    row = findid(ctx.author.id)
    if row is not None:
        sdk_tb, sdk_prize = readsuko(row)
        if sdk_prize == '0':
            await ctx.send("数独をプレイしてないです、$sdkでプレイしてください")
        else:
            cord = cord.upper()
            try:
                ansi = int(ans)
            except:
                await ctx.send("答えは１から９までの数字でお願いします")
                return
            if 9< ansi or ansi < 0:
                await ctx.send("答えは１から９までの数字でお願いします")
                return
            elif cord[0] > cord[1] and len(cord)==2:
                Crow = cord[0]
                Ccol = cord[1]
            elif cord[0] < cord[1] and len(cord)==2:
                Crow = cord[1]
                Ccol = cord[0]
            else:
                await ctx.send("座標がなんかおかしいです")
                return
            try:
                Ccoli = int(Ccol)
            except:
                await ctx.send("座標がなんかおかしいです")
                return
            if 'I'>=Crow>='A' and 9>=Ccoli>=1:
                sdk_tb_n, Errchk = sudoku_ans_set(sdk_tb, Crow, Ccol, ans)
            else:
                await ctx.send("座標がなんかおかしいです")
                return
            if Errchk:
                await ctx.send(f"{Crow}{Ccol}は問題ではないです")
            else:
                savesuko(row, sdk_tb_n, sdk_prize)
                sdk_tb_n, sdk_prize = readsuko(row)
                sdk_str = sudoku_prt_str(sdk_tb_n, sdk_prize, ctx.author.name)
                await ctx.send(sdk_str)
                sched.resume()
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))

@bot.command(aliases=['ans', '答え'])
async def sudoku_ans(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        sdk_tb, sdk_prize = readsuko(row)
        if sdk_prize == '0':
            await ctx.send("数独をプレイしてないです、$sdkでプレイしてください")
        else:
            money, level, cnt, ccnt = rdinf(row)
            # sdk_str = sudoku_prt_str(sdk_tb, sdk_prize, ctx.author.name)
            # await ctx.send(sdk_str)
            if chk_sudoku(sdk_tb):
                edtmny(row, money + int(sdk_prize))
                sdk_emb = discord.Embed(title="大正解", description=f"賞金 : {sdk_prize}"
                                                                    f"\n所持金 : {money}円 -> {money+int(sdk_prize)}円", color=0xC49C48)
                await ctx.send(embed=sdk_emb)
                savesuko(row, 0, 0)
            else:
                if money >= 1000:
                    edtmny(row, money - 1000)
                    sdk_emb = discord.Embed(title="不正解", description=f"賞金 : {sdk_prize}"
                                                                    f"\n所持金 : {money}円 -> {money-1000}円", color=0xD71143)
                    await ctx.send(embed=sdk_emb)
                else:
                    await ctx.send("罰金の1000円がないので数独プレイを中止します")
                    savesuko(row, 0, 0)
            sched.resume()            
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))
        
@bot.command(aliases=['sdk_fail', '諦める'])
async def sudoku_giveup(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        sdk_tb, sdk_prize = readsuko(row)
        if sdk_prize == '0':
            await ctx.send("数独をプレイしてないです、$sdkでプレイしてください")
        else:
            await ctx.send("数独から逃げました、プレイを中止します")
            savesuko(row, 0, 0)
            sched.resume()            
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command()
async def dg(ctx):
    if hex(ctx.author.id) == "0x9e8818f3342007b":
        dataget()
        await ctx.send("データ読み込み完了")
    else:
        await ctx.send("権限がありません")


@bot.command()
async def ds(ctx):
    if hex(ctx.author.id) == "0x9e8818f3342007b":
        datasave()
        await ctx.send("データバックアップ完了")
    else:
        await ctx.send("権限がありません")


@bot.command(aliases=['a', '登録'])
async def account(ctx):
    if findid(ctx.author.id):
        await ctx.send("既にダイスの亡者です。")
    else:
        signup(ctx.author.name, ctx.author.id)
        await ctx.send("ダイスの世界へようこそ！")
        sched.resume()


@bot.command()
async def el(ctx, user: discord.User, lvl):
    row = None
    if hex(ctx.author.id) == "0x9e8818f3342007b":
        row = findid(user.id)
    else:
        await ctx.send("権限がありません")
    if row is not None:
        edtlvl(row, int(lvl))
        await ctx.send("{}のレベルを{}に設定しました".format(user.mention, lvl))
        sched.resume()
    else:
        await ctx.send("{}はダイスの住民ではありません".format(user.mention))


@bot.command()
async def em(ctx, user: discord.User, mny):
    row = None
    if hex(ctx.author.id) == "0x9e8818f3342007b":
        row = findid(user.id)
    else:
        await ctx.send("権限がありません")
    if row is not None:
        edtmny(row, int(mny))
        await ctx.send("{}のお金を{}に設定しました".format(user.mention, mny))
        sched.resume()
    else:
        await ctx.send("{}はダイスの住民ではありません".format(user.mention))


@bot.command()
async def rst(ctx):
    if hex(ctx.author.id) == "0x9e8818f3342007b":
        rstdat()
        await ctx.send("リセット完了")
        sched.resume()
    else:
        await ctx.send("権限がありません")


@bot.command(aliases=['i', '情報'])
async def info(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        money, level, cnt, ccnt = rdinf(row)
        infbed = discord.Embed(title="ユーザー名", description=ctx.author.name, color=0xE67A3F)
        infbed.add_field(name="所持金", value=f"{money}円", inline=False)
        infbed.add_field(name="ダイス強化レベル", value=f"＋{level}", inline=False)
        infbed.add_field(name="カジノ出勤回数", value="{}回".format(ccnt), inline=False)
        seme, uke = battler(row)
        if (seme != 0) and (uke != 0):
            s_name = getname(seme)
            u_name = getname(uke)
            infbed.add_field(name="果たし状", value=f"{s_name}に出して、{u_name}から貰ってます。", inline=False)
        elif seme != 0:
            s_name = getname(seme)
            infbed.add_field(name="果たし状", value=f"{s_name}に出してます。", inline=False)
        elif uke != 0:
            u_name = getname(uke)
            infbed.add_field(name="果たし状", value=f"{u_name}から貰ってます。", inline=False)
        infbed.set_footer(text=f"ダイスの出目が{level**2}されます。")
        await ctx.send(embed=infbed)
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['io', '他人情報'])
async def infoother(ctx, user: discord.User):
    row = findid(user.id)
    if row is not None:
        money, level, cnt, ccnt = rdinf(row)
        infbed = discord.Embed(title="ユーザー名", description=user.name, color=0xE67A3F)
        infbed.add_field(name="保有資金", value=str(money) + "円", inline=False)
        infbed.add_field(name="ダイス強化レベル", value="＋" + str(level), inline=False)
        infbed.add_field(name="カジノ出勤回数", value="{}回".format(ccnt), inline=False)
        seme, uke = battler(row)
        if (seme != 0) and (uke != 0):
            s_name = getname(seme)
            u_name = getname(uke)
            infbed.add_field(name="果たし状", value=f"{s_name}に出して、{u_name}から貰ってます。", inline=False)
        elif seme != 0:
            s_name = getname(seme)
            infbed.add_field(name="果たし状", value=f"{s_name}に出してます。", inline=False)
        elif uke != 0:
            u_name = getname(uke)
            infbed.add_field(name="果たし状", value=f"{u_name}から貰ってます。", inline=False)
        infbed.set_footer(text="ダイスの出目が＋" + str(level ** 2) + "されます。")
        await ctx.send(embed=infbed)
    else:
        await ctx.send("{}はダイスの住民ではありません".format(user.mention))


@bot.command(aliases=['kh', '確率'])
async def enchantper(ctx):
    perbed = discord.Embed(title="ダイス強化確率", description="強化効果:ダイスの出目が強化数値^2プラスされます。", color=0xE67A3F)
    perbed.add_field(name="+0 -> +1", value="成功90%、失敗(維持)10%", inline=False)
    perbed.add_field(name="+1 -> +2", value="成功80%、失敗(維持)15%、失敗(-1)5%", inline=False)
    perbed.add_field(name="+2 -> +3", value="成功70%、失敗(維持)20%、失敗(-1)10%", inline=False)
    perbed.add_field(name="+3 -> +4", value="成功60%、失敗(維持)25%、失敗(-1)15%", inline=False)
    perbed.add_field(name="+4 -> +5", value="成功50%、失敗(維持)30%、失敗(-1)20%", inline=False)
    perbed.add_field(name="+5 -> +6", value="成功40%、失敗(維持)35%、失敗(-1)25%", inline=False)
    perbed.add_field(name="+6 -> +7", value="成功30%、失敗(維持)40%、失敗(-1)30%", inline=False)
    perbed.add_field(name="+7 -> +8", value="成功20%、失敗(維持)45%、失敗(-1)35%", inline=False)
    perbed.add_field(name="+8 -> +9", value="成功10%、失敗(維持)50%、失敗(-1)40%", inline=False)
    perbed.add_field(name="+9 -> +10", value="成功10%、失敗(維持)45%、失敗(-1)40%、失敗(リセット)5%", inline=False)
    perbed.add_field(name="+10 -> +11", value="成功10%、失敗(維持)40%、失敗(-1)40%、失敗(リセット)10%", inline=False)
    perbed.add_field(name="+11 -> +12", value="成功10%、失敗(維持)35%、失敗(-1)40%、失敗(リセット)15%", inline=False)
    perbed.add_field(name="+12 -> +13", value="成功10%、失敗(維持)30%、失敗(-1)40%、失敗(リセット)20%", inline=False)
    perbed.add_field(name="+13 -> +14", value="成功10%、失敗(維持)25%、失敗(-1)40%、失敗(リセット)25%", inline=False)
    perbed.add_field(name="+14 -> +15", value="成功10%、失敗(維持)20%、失敗(-1)40%、失敗(リセット)30%", inline=False)
    perbed.add_field(name="+15 -> +16", value="成功10%、失敗(維持)15%、失敗(-1)40%、失敗(リセット)35%", inline=False)
    perbed.add_field(name="+16 -> +17", value="成功10%、失敗(維持)10%、失敗(-1)40%、失敗(リセット)40%", inline=False)
    perbed.add_field(name="+17 -> +18", value="成功10%、失敗(維持)5%、失敗(-1)40%、失敗(リセット)45%", inline=False)
    perbed.add_field(name="+18 -> +19", value="成功10%、失敗(-1)40%、失敗(リセット)50%", inline=False)
    perbed.add_field(name="+19 -> +20", value="成功10%、失敗(-1)35%、失敗(リセット)55%", inline=False)
    perbed.add_field(name="+20 -> +21", value="成功10%、失敗(-1)30%、失敗(リセット)60%", inline=False)
    perbed.add_field(name="+21 -> +22", value="成功10%、失敗(-1)25%、失敗(リセット)65%", inline=False)
    perbed.add_field(name="+22 -> +23", value="成功10%、失敗(-1)20%、失敗(リセット)70%", inline=False)
    perbed.add_field(name="+23 -> +24", value="成功10%、失敗(-1)15%、失敗(リセット)75%", inline=False)
    perbed.add_field(name="+24 -> +25", value="成功10%、失敗(-1)10%、失敗(リセット)80%", inline=False)
    perbed.add_field(name="+25 -> +26", value="成功10%、失敗(-1)5%、失敗(リセット)85%", inline=False)
    perbed.add_field(name="+26 -> +27", value="成功10%、失敗(リセット)90%", inline=False)
    perbed.add_field(name="+27 ~ ", value="成功5%、失敗(リセット)95%", inline=False)
    await ctx.send(embed=perbed)


@bot.command(aliases=['k', '強化'])
async def enchant(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        seme, uke = battler(row)
        if (seme == 0) and (uke == 0):
            money, level, cnt, ccnt = rdinf(row)
            if money < 100:
                await ctx.send("金欠なのでガチャガチャできません、100円集めて来なさい")
            else:
                macnted(row, 3)
                edtmny(row, money-100)
                mamny = mazinkin()
                mazinkined(mamny + 100)
                reslt = enchnt(level)
                if reslt == 1:
                    edtlvl(row, level+1)
                    await ctx.send("強化成功！！、{}のダイスが＋{}に強化されました！\n所持金が{}円残りました。".format(ctx.author.mention,
                                                                                      str(level+1), str(money-100)))
                elif reslt == 2:
                    edtlvl(row, level-1)
                    await ctx.send("強化失敗！、{}のダイスの強化段階が＋{}に下がりました！\n所持金が{}円残りました。".format(ctx.author.mention,
                                                                                         str(level-1), str(money-100)))
                elif reslt == 3:
                    edtlvl(row, 0)
                    await ctx.send("強化失敗！！、{}のダイスが粉々に砕けました！\n所持金が{}円残りました。".format(ctx.author.mention,
                                                                                   str(money-100)))
                else:
                    await ctx.send("強化失敗、{}は何も得られませんでした。\n所持金が{}円残りました。".format(ctx.author.mention,
                                                                                str(money-100)))
            sched.resume()
        else:
            await ctx.send("果たし状を処理するまでは強化できません。")
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['sk', 'スペシャル強化'])
async def specialenchant(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        money, level, cnt, ccnt = rdinf(row)
        seme, uke = battler(row)
        if (seme == 0) and (uke == 0):
            if level < 6:
                await ctx.send("スペシャル強化は＋6以上からしましょう、勿体ないです。")
            else:
                if level < 18:
                    daikin = level * 500
                    if daikin == 0:
                        daikin = 500
                else:
                    daikin = level * 1000
                if money < daikin:
                    await ctx.send("スペシャル強化には{}円必要です。".format(daikin))
                else:
                    macnted(row, 3)
                    edtmny(row, money-daikin)
                    mamny = mazinkin()
                    faild = dihyaku()
                    reslt = enchnt(level)
                    if faild == 100 and (reslt == 3):
                        edtlvl(row, level - 3)
                        await ctx.send("ファンブル！！、{}は土下座しようとしたんですが間違ってダイスを踏みつぶしました。\nダイスの強化段階が＋{}まで下がりました。"
                                       "\n所持金が{}円残りました。".format(ctx.author.mention, str(level - 3), str(money-daikin)))
                    else:
                        if reslt == 1:
                            edtlvl(row, level+1)
                            await ctx.send("強化成功！！、{}のダイスが＋{}に強化されました！\n所持金が{}円残りました。"
                                           .format(ctx.author.mention, str(level+1), str(money-daikin)))
                        elif reslt == 2:
                            mazinkined(mamny + daikin // 2)
                            await ctx.send("強化失敗！、{}のダイスの強化段階が＋{}に下がりそうだったけど媚びを売って何とか防げました！"
                                           "\n所持金が{}円残りました。".format(ctx.author.mention,
                                                                    str(level-1), str(money-daikin)))
                        elif reslt == 3:
                            mazinkined(mamny + daikin // 2)
                            await ctx.send("強化失敗！！、{}のダイスが粉々に砕けそうだったけど土下座して何とか免れました！"
                                           "\n所持金が{}円残りました。".format(ctx.author.mention, str(money-daikin)))
                        else:
                            mazinkined(mamny + daikin)
                            await ctx.send("強化失敗、{}は何も得られませんでした。\n所持金が{}円残りました。"
                                           .format(ctx.author.mention, str(money-daikin)))
            sched.resume()
        else:
            await ctx.send("果たし状を処理するまでは強化できません。")
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['kk', '連続強化'])
async def enchantren(ctx, num):
    if int(num) <= 25:
        row = findid(ctx.author.id)
        if row is not None:
            seme, uke = battler(row)
            if (seme == 0) and (uke == 0):
                kyobed = discord.Embed(title="{}連強化".format(num), description="強化スタート！", color=0x000000)
                money, level, cnt, ccnt = rdinf(row)
                if money < 100*int(num):
                    await ctx.send("そんなに回せるお金ないやんか！")
                else:
                    macnted(row, 3)
                    for i in range(1, int(num)+1):
                        money, level, cnt, ccnt = rdinf(row)
                        edtmny(row, money - 100)
                        mamny = mazinkin()
                        mazinkined(mamny+100)
                        reslt = enchnt(level)
                        if reslt == 1:
                            edtlvl(row, level + 1)
                            kyobed.add_field(name="{}回目".format(str(i)), value="強化成功！！、{}のダイスが＋{}に強化されました！"
                                                                               "\n所持金が{}円残りました。"
                                             .format(ctx.author.name, str(level + 1), str(money - 100)), inline=False)
                        elif reslt == 2:
                            edtlvl(row, level - 1)
                            kyobed.add_field(name="{}回目".format(str(i)), value="強化失敗！、{}のダイスの強化段階が＋{}に下がりました！"
                                                                               "\n所持金が{}円残りました。"
                                             .format(ctx.author.name, str(level - 1), str(money - 100)), inline=False)
                        elif reslt == 3:
                            edtlvl(row, 0)
                            kyobed.add_field(name="{}回目".format(str(i)), value="強化失敗！！、{}のダイスが粉々に砕けました！"
                                                                               "\n所持金が{}円残りました。"
                                             .format(ctx.author.name, str(money - 100)), inline=False)
                        else:
                            kyobed.add_field(name="{}回目".format(str(i)), value="強化失敗、{}は何も得られませんでした。"
                                                                               "\n所持金が{}円残りました。"
                                             .format(ctx.author.name, str(money - 100)), inline=False)
                    await ctx.send(embed=kyobed)
                    money, level, cnt, ccnt = rdinf(row)
                    await ctx.send("{}のダイスは＋{}になった！".format(ctx.author.mention, str(level)))
                sched.resume()
            else:
                await ctx.send("果たし状を処理するまでは強化できません。")
        else:
            await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))
    else:
        await ctx.send("25回以下でお願いします、死にそうです。")


@bot.command(aliases=['im', '魔人情報'])
async def mazininfo(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        mamny = mazinkin()
        mazki = mazinki(row)
        if mazki < 0:
            botlvl = calbotlvl() + (mazki // 2) + 1
        else:
            botlvl = calbotlvl() + (mazki // 2)
        # botlvl -= mamny//10000
        if botlvl < 0:
            botlvl = 0
        mazbed = discord.Embed(title="ユーザー名", description="ダイスの魔人", color=0xE67A3F)
        mazbed.add_field(name="所持金", value=str(mamny) + "円", inline=False)
        if botlvl < calbotlvl():
            mazbed.add_field(name="ダイス強化レベル", value="ご機嫌なのであなたに優しくなってます\n＋" + str(botlvl), inline=False)
        elif botlvl > calbotlvl():
            mazbed.add_field(name="ダイス強化レベル", value="あなたに激おこなので厳しくなってます\n＋" + str(botlvl), inline=False)
        else:
            mazbed.add_field(name="ダイス強化レベル", value="＋" + str(botlvl), inline=False)
        mazbed.set_footer(text="ダイスの出目が＋" + str(botlvl ** 2) + "されます。")
        await ctx.send(embed=mazbed)
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['v', 'bot戦'])
async def vsbot(ctx, bat = -99):
    row = findid(ctx.author.id)
    if row is not None:
        money, level, cnt, ccnt = rdinf(row)
        you_jan, maz_jan, prise_jan = readjanken(row)
        if int(cnt) > 0:
            if you_jan == '0':
                if int(bat) <= 0:
                    await ctx.send("少なくとも1円以上は掛けないと...")
                else:
                    mamny = mazinkin()
                    if money < int(bat):
                        await ctx.send("所持金が{}円より少ないわよ！コラァ！！！".format(bat))
                    elif mamny < int(bat):
                        await ctx.send("魔人の所持金は{}円しかないです、いじめないでください。".format(str(mamny)))
                    else:
                        
                        if you_jan == '0':
                            you_jan = setdeck()
                            maz_jan = setdeck()
                            prise_jan = bat
                        
                    '''
                    # kigen = mazinki(row)
                    # if kigen < 0:
                    #     botlvl = calbotlvl()+(kigen//2)+1
                    #     if botlvl < 0:
                    #         botlvl = 0
                    # else:
                    #     botlvl = calbotlvl()+(kigen//2)
                    # mamny = mazinkin()
                    # # botlvl -= mamny // 10000
                    # if botlvl < 0:
                    #     botlvl = 0
                    # macnted(row, cnt - 1)
                    # rslt, dcpl, dcbt = vsbt(level, botlvl)
                    # if rslt == 0 or rslt == 3:
                    #     botbed = discord.Embed(title="VS 魔人戦", description="引き分け！", color=0xFFFFFF)
                    # elif rslt == 1 or rslt == 4:
                    #     edtmny(row, money+int(bat))
                    #     mazinkined(mamny-int(bat))
                    #     mazinkied(row, kigen+1)
                    #     botbed = discord.Embed(title="VS 魔人戦", description="あなたの勝ち！", color=0xB9E3FC)
                    # else:
                    #     edtmny(row, money-int(bat))
                    #     mazinkined(mamny+int(bat))
                    #     mazinkied(row, kigen-1)
                    #     botbed = discord.Embed(title="VS 魔人戦", description="あなたの負け！", color=0xFFE0F5)
                    # if rslt == 3:
                    #     if dcbt == 1:
                    #         edtmny(row, money + ceil(int(bat)/2))
                    #         mazinkined(mamny + ceil(int(bat)/2))
                    #         botbed.add_field(name="双方勝利！", value="二人とも出目:{}".format(dcbt), inline=False)
                    #     if dcbt == 100:
                    #         edtmny(row, money - ceil(int(bat)/2))
                    #         mazinkined(mamny - ceil(int(bat)/2))
                    #         botbed.add_field(name="双方敗北！", value="二人とも出目:{}".format(dcbt), inline=False)
                    # else:
                    #     if dcbt == 1:
                    #         botbed.add_field(name="ダイスの魔人", value="出目:{}\n確定勝利".format(dcbt))
                    #     elif dcbt == 100:
                    #         botbed.add_field(name="ダイスの魔人", value="出目:{}\n確定敗北".format(dcbt))
                    #     else:
                    #         botbed.add_field(name="ダイスの魔人", value="出目:{}＋ダイス効果:{}\n合計:{}"
                    #                          .format(dcbt, botlvl**2, (botlvl**2)+dcbt))
                    #     if dcpl == 1:
                    #         botbed.add_field(name="あなた", value="出目:{}\n確定勝利".format(dcpl))
                    #     elif dcpl == 100:
                    #         botbed.add_field(name="あなた", value="出目:{}\n確定敗北".format(dcpl))
                    #     else:
                    #         botbed.add_field(name="あなた", value="出目:{}＋ダイス効果:{}\n合計:{}"
                    #                          .format(dcpl, level**2, (level**2)+dcpl))
                    # money2, level, cnt2, ccnt = rdinf(row)
                    # mamny2 = mazinkin()
                    # botbed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
                    # botbed.add_field(name="魔人の所持金", value="{}円 -> {}円".format(mamny, mamny2), inline=False)
                    # botbed.add_field(name="残りの魔人への挑戦回数", value="{}回 -> {}回".format(cnt, cnt2), inline=False)
                    # if botlvl > calbotlvl():
                    #     botbed.add_field(name="魔人はあなたに激おこぷんぷん丸です", value="魔人のダイスが＋{}されます"
                    #                      .format(botlvl - calbotlvl()), inline=False)
                    # elif botlvl < calbotlvl():
                    #     botbed.add_field(name="魔人はあなたに仏様のような笑みを見せてます", value="魔人のダイスが-{}されます"
                    #                      .format(calbotlvl() - botlvl), inline=False)
                    # botbed.set_footer(text="魔人のダイス:＋{}(プレイヤーの強化平均値 + 魔人の機嫌補正)".format(botlvl))
                    # await ctx.send(embed=botbed)
                    '''
                sched.resume()
                
            
                
        else:
            await ctx.send("魔人いじめはもうやめて強化しに行こう？")
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['d', 'ダイス当て'])
async def diceate(ctx, ans, bat):
    if 1 <= int(ans) <= 100:
        row = findid(ctx.author.id)
        if row is not None:
            money, level, cnt, ccnt = rdinf(row)
            if money >= int(bat):
                mamny = mazinkin()
                mazinkined(mamny + 100)
                da = dihyaku()
                if da == int(ans):
                    edtmny(row, money + (int(bat) * 18))
                    diabed = discord.Embed(title="大当たり", description=f"100面ダイスの出目を当てよう！"
                                                                     f"\n掛け金 : {bat}円 x 18倍", color=0xC49C48)
                elif (da % 2 == 0 and int(ans) % 2 == 0) or (da % 2 == 1 and int(ans) % 2 == 1):
                    edtmny(row, money + ceil(int(bat) * 0.6))
                    diabed = discord.Embed(title="勝　利", description="100面ダイスの出目を当てよう！"
                                                                    "\n掛け金 : {}円 x 0.6倍".format(bat), color=0x06508D)
                else:
                    edtmny(row, money - int(bat))
                    diabed = discord.Embed(title="敗　北", description="100面ダイスの出目を当てよう！"
                                                                    "\n掛け金 : {}円".format(bat), color=0xD71143)
                    # mamny = mazinkin()
                    # mazinkined(mamny + int(bat)//2)
                if da % 2 == 0:
                    diabed.add_field(name="ダイスの出目", value="{}  偶数".format(da))
                else:
                    diabed.add_field(name="ダイスの出目", value="{}  奇数".format(da))
                if int(ans) % 2 == 1:
                    diabed.add_field(name="{}の予想".format(ctx.author.name), value=f"{ans}  奇数")
                else:
                    diabed.add_field(name="{}の予想".format(ctx.author.name), value=f"{ans}  偶数")
                money2, level, cnt, ccnt = rdinf(row)
                diabed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
                cscnt = cascnt(row)
                await ctx.send(embed=diabed)
                if (cscnt + 1) % 1000 == 0:
                    money, level, cnt, ccnt = rdinf(row)
                    edtmny(row, money + ((cscnt + 1) * 10))
                    await ctx.send("実績解禁！！\n{}はカジノに{}回通いました。\n頑張ったから{}円あげちゃう"
                                   .format(ctx.author.mention, cscnt + 1, (cscnt + 1) * 10))
                sched.resume()
            else:
                await ctx.send("{}は有り金全部溶かしたので、{}円なんて出せないです".format(ctx.author.mention, bat))
        else:
            await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))
    else:
        await ctx.send("1~100の中で選んでください")


@bot.command(aliases=['c', 'カジノ'])
async def casino(ctx):
    row = findid(ctx.author.id)
    if row is not None:
        dc = csno()
        cn = csnonum()
        ck = csnokin()
        csnokined(ck+100)
        mamny = mazinkin()
        mazinkined(mamny+100)
        ck = csnokin()
        if dc == cn:
            money, level, cnt, ccnt = rdinf(row)
            edtmny(row, money+ck+100)
            money2, level, cnt, ccnt = rdinf(row)
            csnorst()
            csnokined(10000)
            ck2 = csnokin()
            cn2 = csnonum()
            casbed = discord.Embed(title="JACKPOT!!!!!!!!", description=f"1/1000の確率に勝ってウハウハに儲けよう！"
                                                                        f"\n賞金:{ck+100}円 -> {ck2}円", color=0xFF017E)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            casbed.add_field(name="結果", value="{}".format(dc), inline=False)
            casbed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
            casbed.add_field(name="次のJackpot Number", value="{}".format(cn2), inline=False)
        elif dc == 80:
            casbed = discord.Embed(title="はおー！！", description="1/1000の確率に勝ってウハウハに儲けよう！"
                                                              "\n賞金:{}円".format(ck), color=0xFFA4D1)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            casbed.add_field(name="結果", value="{}".format(dc), inline=False)
            money, level, cnt, ccnt = rdinf(row)
            edtmny(row, money + 8080)
            money2, level, cnt, ccnt = rdinf(row)
            casbed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
        elif dc == 777:
            casbed = discord.Embed(title="ラッキーセブン！", description="1/1000の確率に勝ってウハウハに儲けよう！"
                                                                 "\n賞金:{}円".format(ck), color=0xFFFF00)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            ck7 = ceil(ck/1000)*300
            money, level, cnt, ccnt = rdinf(row)
            edtmny(row, money + ck7)
            money2, level, cnt, ccnt = rdinf(row)
            casbed.add_field(name="結果", value="{}".format(dc), inline=False)
            casbed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
        elif dc == 1:
            money, level, cnt, ccnt = rdinf(row)
            edtmny(row, money + 5000)
            money2, level, cnt, ccnt = rdinf(row)
            casbed = discord.Embed(title="ダイスルーレット", description="1/1000の確率に勝ってウハウハに儲けよう！"
                                                                 "\n賞金:{}円".format(ck), color=0xFFFFFF)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            casbed.add_field(name="結果", value="{}\nクリティカル！".format(dc), inline=False)
            casbed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
        elif (dc < 100 and dc % 11 == 0) or dc % 111 == 0:
            money, level, cnt, ccnt = rdinf(row)
            edtmny(row, money + 1000)
            money2, level, cnt, ccnt = rdinf(row)
            casbed = discord.Embed(title="ダイスルーレット", description="1/1000の確率に勝ってウハウハに儲けよう！"
                                                                 "\n賞金:{}円".format(ck), color=0x7F7F7F)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            casbed.add_field(name="結果", value="{}\nぞろ目！".format(dc), inline=False)
            casbed.add_field(name="あなたの所持金", value="{}円 -> {}円".format(money, money2), inline=False)
        elif dc == 1000:
            mazinkined(mamny + 100+ck//4)
            csnokined((ck + 100)//2)
            ck2 = csnokin()
            await ctx.send("{}様、{}円、ありがとうございます。".format(ctx.author.mention, ck//4))
            casbed = discord.Embed(title="ダイスルーレット", description=f"1/1000の確率に勝ってウハウハに儲けよう！\n"
                                                                 f"賞金:{ck+100}円 -> {ck2}円", color=0x000000)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            casbed.add_field(name="結果", value="{}\nファンブル！".format(dc), inline=False)
        else:
            casbed = discord.Embed(title="ダイスルーレット", description="1/1000の確率に勝ってウハウハに儲けよう！"
                                                                 "\n賞金:{}円".format(ck), color=0xFBE382)
            casbed.add_field(name="Jackpot Number", value="{}".format(cn), inline=False)
            casbed.add_field(name="参加者", value="{}".format(ctx.author.name), inline=False)
            casbed.add_field(name="結果", value="{}\nはっずれ～".format(dc), inline=False)
        cscnt = cascnt(row)
        await ctx.send(embed=casbed)
        if (cscnt+1) % 1000 == 0:
            money, level, cnt, ccnt = rdinf(row)
            edtmny(row, money + ((cscnt+1)*20))
            await ctx.send("実績解禁！！\n{}はカジノに{}回通いました。\n頑張ったから{}円あげちゃう"
                           .format(ctx.author.mention, cscnt+1, (cscnt+1)*20))
        sched.resume()
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['b', 'バトル'])
async def battle(ctx, dice):
    if int(dice) < 2:
        await ctx.send("それ本当にダイスなの？")
    else:
        row = findid(ctx.author.id)
        if row is not None:
            money, level, cnt, ccnt = rdinf(row)
            dc = batdice(int(dice))
            await ctx.send("使用ダイス:{}面ダイス\n{}の出目:{}＋ダイスの効果:{}\n合計:{}"
                           .format(dice, ctx.author.mention, dc, level**2, dc+(level**2)))
            sched.resume()
        else:
            await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['s', '送金'])
async def sendmoney(ctx, user: discord.User, mny):
    if int(mny) <= 0:
        await ctx.send("送金出来そうな金額を入れて！")
    else:
        row = findid(ctx.author.id)
        row2 = findid(user.id)
        if row2 is not None:
            if row is not None:
                if row == row2:
                    await ctx.send("自分には送金出来ないわよ。")
                else:
                    money, level, cnt, ccnt = rdinf(row)
                    if money >= int(mny):
                        money2, level, cnt, ccnt = rdinf(row2)
                        edtmny(row, money-int(mny))
                        edtmny(row2, money2+int(mny))
                        senbed = discord.Embed(title="送金成功", description="{}に{}円を送金しました。"
                                               .format(user.name, mny), color=0x5E6482)
                        senbed.add_field(name="あなたの所持金", value="{}円".format(str(money-int(mny))))
                        senbed.add_field(name="{}の所持金".format(user.name), value="{}円".format(str(money2+int(mny))))
                        await ctx.send(embed=senbed)
                        sched.resume()
                    else:
                        await ctx.send("{}は貧乏過ぎて送金出来ません".format(ctx.author.mention))
        else:
            if row is not None:
                await ctx.send("{}はダイスの住民ではありません".format(user.mention))
            else:
                await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['rank', 'ランキング'])
async def ranking(ctx):
    rows = rank()
    # print(rows)
    # rk = 1
    # er = 1
    # while er != 0:
    #     for _row in rows:
    #         er = 0
    #         if rk > 1:
    #             if int(_row[rk-2][1][0]) == int(_row[rk-1][1][0]):
    #                 if int(_row[rk-2][1][1]) < int(_row[rk-1][1][1]):
    #                     rows[rk-2], rows[rk-1] = rows[rk-1], rows[rk-2]
    #                     er += 1
    #         rk += 1
    ranbed = discord.Embed(title="ランキング　TOP5", description="レベルが同じ場合、 所持金で比較", color=0x22B14C)
    for idx in range(1, 6):
        ranbed.add_field(name="{}位　{}".format(idx, rows[idx-1][0]), value="ダイス強化 : ＋{}\n所持金 : {}円"
                         .format(rows[idx-1][1][0], rows[idx-1][1][1]), inline=False)
    await ctx.send(embed=ranbed)


@bot.command(aliases=['h', '果たし状'])
async def hatasijou(ctx, user: discord.User):
    row = findid(ctx.author.id)
    row2 = findid(user.id)
    if (row is not None) and (row2 is not None):
        deki = battlew(row, row2)
        if deki:
            await ctx.send(f"{ctx.author.mention}は{user.mention}に果たし状を出しました。")
        else:
            await ctx.send(f"既に誰かとバトルの準備をしてます。")
        sched.resume()
    elif row is None:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))
    else:
        await ctx.send("{}はダイスの住民ではありません".format(user.mention))


@bot.command(aliases=['u', '受けて立つ'])
async def uketetatsu(ctx, dicemen, money):
    row = findid(ctx.author.id)
    if row is not None:
        seme, uke = battler(row)
        if uke != 0:
            u_money, u_level, cnt, ccnt = rdinf(row)
            s_money, s_level, cnt, ccnt = rdinf(uke)
            batmny = min(int(money), u_money, s_money)
            u_dice = batdice(int(dicemen))
            s_dice = batdice(int(dicemen))
            s_name = getname(uke)
            u_name = ctx.author.name
            batbed = discord.Embed(title="ダイスバトル！", description=f"挑戦者 : {s_name}   保守者 : {u_name}",
                                   color=0x542200)
            if s_dice == 1:
                batbed.add_field(name=f"{s_name}", value="出目:1\n確定勝利")
            elif s_dice == int(dicemen):
                batbed.add_field(name=f"{s_name}", value=f"出目:{s_dice}\n確定敗北")
            else:
                batbed.add_field(name=f"{s_name}", value=f"出目:{s_dice}＋ダイス効果:{s_level ** 2}\n合計:"
                                                         f"{s_dice + (s_level ** 2)}")
            if u_dice == 1:
                batbed.add_field(name=f"{u_name}", value="出目:1\n確定勝利")
            elif u_dice == int(dicemen):
                batbed.add_field(name=f"{u_name}", value=f"出目:{u_dice}\n確定敗北")
            else:
                batbed.add_field(name=f"{u_name}", value=f"出目:{u_dice}＋ダイス効果:{u_level ** 2}\n"
                                                         f"合計:{u_dice + (u_level ** 2)}")
            if (u_dice == s_dice == 1) or (u_dice == s_dice == int(dicemen)) or ((s_dice + (s_level ** 2)) ==
                                                                                 (u_dice + (u_level ** 2))):
                batbed.add_field(name="対戦結果", value="引き分け", inline=False)
            elif (s_dice == 1) or (u_dice == int(dicemen)) or (u_dice + (u_level ** 2)) < (s_dice + (s_level ** 2)):
                batbed.add_field(name="対戦結果", value=f"{s_name}の勝ち", inline=False)
                edtmny(row, u_money - batmny)
                edtmny(uke, s_money + batmny)
                batbed.add_field(name=f"{s_name}の所持金", value=f"{s_money}円 -> {s_money + batmny}円")
                batbed.add_field(name=f"{u_name}の所持金", value=f"{u_money}円 -> {u_money - batmny}円")
            else:
                batbed.add_field(name="対戦結果", value=f"{u_name}の勝ち", inline=False)
                edtmny(row, u_money + batmny)
                edtmny(uke, s_money - batmny)
                batbed.add_field(name=f"{s_name}の所持金", value=f"{s_money}円 -> {s_money - batmny}円")
                batbed.add_field(name=f"{u_name}の所持金", value=f"{u_money}円 -> {u_money + batmny}円")
            battlee(uke, row)
            await ctx.send(embed=batbed)
            sched.resume()
        else:
            await ctx.send("{}は誰からでも果たし状を受けてません".format(ctx.author.mention))
    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))


@bot.command(aliases=['bc', 'バカラ'])
async def baccarat(ctx, batrslt, batting):
    row = findid(ctx.author.id)
    if row is not None:
        if batrslt == 't' or batrslt == 'T' or batrslt == 'p' or batrslt == 'P' or batrslt == 'b' or batrslt == 'B':
            mamny = mazinkin()
            mazinkined(mamny + 100)
            if batrslt == 'T':
                batrslt = 't'
            if batrslt == 'P':
                batrslt = 'p'
            if batrslt == 'B':
                batrslt = 'b'
            uname = getname(row)
            pc, bc, result, pce, bce = bac()
            money, level, cnt, ccnt = rdinf(row)
            batmny = min(money, int(batting))
            await ctx.send(f"{ctx.author.mention}は '{pc[0][0]+str(pc[0][1])}' と '{pc[1][0]+str(pc[1][1])}' を引きました。")
            await ctx.send(f"バンカーは '{bc[0][0] + str(bc[0][1])}' と '{bc[1][0] + str(bc[1][1])}' を引きました。")
            if result == batrslt:
                bacbed = discord.Embed(title="バカラ", description="あなたの勝ち！", color=0xB6E4FE)
                if batrslt == 't':
                    edtmny(row, money+(int(batmny)*8))
                elif batrslt == 'p':
                    edtmny(row, money + int(batmny))
                else:
                    edtmny(row, money + ceil(int(batmny)*0.95))
            else:
                bacbed = discord.Embed(title="バカラ", description="あなたの負け！", color=0xFEE1F5)
                edtmny(row, money - int(batmny))
            if len(pc) > 2:
                await ctx.send(f"{ctx.author.mention}は '{pc[2][0] + str(pc[2][1])}' を引きました。")
                bacbed.add_field(name=f"{uname}のカード", value=f"{pc[0][0]+str(pc[0][1])}\n"
                                                            f"{pc[1][0]+str(pc[1][1])}\n{pc[2][0] + str(pc[2][1])}")
            else:
                await ctx.send(f"{ctx.author.mention} スタンド")
                bacbed.add_field(name=f"{uname}のカード",
                                 value=f"{pc[0][0] + str(pc[0][1])}\n{pc[1][0] + str(pc[1][1])}")
            if len(bc) > 2:
                await ctx.send(f"バンカーは '{bc[2][0] + str(bc[2][1])}' を引きました。")
                bacbed.add_field(name=f"バンカーのカード",
                                 value=f"{bc[0][0] + str(bc[0][1])}\n{bc[1][0] + str(bc[1][1])}"
                                       f"\n{bc[2][0] + str(bc[2][1])}")
            else:
                await ctx.send(f"バンカー スタンド")
                bacbed.add_field(name=f"バンカーのカード",
                                 value=f"{bc[0][0] + str(bc[0][1])}\n{bc[1][0] + str(bc[1][1])}")
            money2, level, cnt, ccnt = rdinf(row)
            bacbed.add_field(name=f"ガードの合計", value=f"{uname}:{pce}\nバンカー:{bce}", inline=False)
            if batrslt == 'p':
                bacbed.add_field(name=f"あなたの賭け", value=f"{uname}の勝利に{batmny}円")
            elif batrslt == 'b':
                bacbed.add_field(name=f"あなたの賭け", value=f"バンカーの勝利に{batmny}円")
            else:
                bacbed.add_field(name=f"あなたの賭け", value=f"タイ(引き分け)に{batmny}円")
            bacbed.add_field(name=f"{uname}の所持金", value=f"{money}円 -> {money2}円", inline=False)
            await ctx.send(embed=bacbed)
            cscnt = cascnt(row)
            if (cscnt + 1) % 1000 == 0:
                money, level, cnt, ccnt = rdinf(row)
                edtmny(row, money + ((cscnt + 1) * 20))
                await ctx.send("実績解禁！！\n{}はカジノに{}回通いました。\n頑張ったから{}円あげちゃう"
                               .format(ctx.author.mention, cscnt + 1, (cscnt + 1) * 20))
            sched.resume()
        else:
            await ctx.send("プレイヤー(p)か、バンカー(b)か、タイ(t)に賭けてください")

    else:
        await ctx.send("{}はダイスの住民ではありません".format(ctx.author.mention))

# keep_alive()
bot.run(token)
