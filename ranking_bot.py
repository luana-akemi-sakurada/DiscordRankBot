import discord
import json
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Bot is ready to track player rankings!')

@bot.command(name='addpoints')
@commands.has_permissions(administrator=True)
async def add_points(ctx, member: discord.Member, points: int):
    """Add points to a member's score (Admin only)"""
    leaderboard = load_leaderboard()
    user_id = str(member.id)
    
    if user_id in leaderboard:
        leaderboard[user_id]['points'] += points
    else:
        leaderboard[user_id] = {
            'name': member.display_name,
            'points': points
        }
    
    save_leaderboard(leaderboard)
    await ctx.send(f"Added {points} points to {member.mention}. Their total is now {leaderboard[user_id]['points']} points.")

@bot.command(name='removepoints')
@commands.has_permissions(administrator=True)
async def remove_points(ctx, member: discord.Member, points: int):
    """Remove points from a member's score (Admin only)"""
    leaderboard = load_leaderboard()
    user_id = str(member.id)
    
    if user_id in leaderboard:
        leaderboard[user_id]['points'] -= points
        if leaderboard[user_id]['points'] < 0:
            leaderboard[user_id]['points'] = 0
        save_leaderboard(leaderboard)
        await ctx.send(f"Removed {points} points from {member.mention}. Their total is now {leaderboard[user_id]['points']} points.")
    else:
        await ctx.send(f"{member.mention} is not in the leaderboard yet.")

@bot.command(name='setpoints')
@commands.has_permissions(administrator=True)
async def set_points(ctx, member: discord.Member, points: int):
    """Set a member's score to a specific value (Admin only)"""
    leaderboard = load_leaderboard()
    user_id = str(member.id)
    
    leaderboard[user_id] = {
        'name': member.display_name,
        'points': points
    }
    
    save_leaderboard(leaderboard)
    await ctx.send(f"Set {member.mention}'s points to {points}.")

@bot.command(name='give')
async def give_points(ctx, member: discord.Member, points: int):
    """Give some of your points to another member"""
    if member.id == ctx.author.id:
        await ctx.send("You can't give points to yourself!")
        return
    
    if points <= 0:
        await ctx.send("You must give a positive number of points!")
        return
    
    leaderboard = load_leaderboard()
    giver_id = str(ctx.author.id)
    receiver_id = str(member.id)
    
    if giver_id not in leaderboard or leaderboard[giver_id]['points'] < points:
        await ctx.send("You don't have enough points to give!")
        return
    
    leaderboard[giver_id]['points'] -= points
    
    if receiver_id in leaderboard:
        leaderboard[receiver_id]['points'] += points
    else:
        leaderboard[receiver_id] = {
            'name': member.display_name,
            'points': points
        }
    
    save_leaderboard(leaderboard)
    await ctx.send(f"🎁 {ctx.author.mention} gave {points} points to {member.mention}!\n"
                   f"{ctx.author.display_name} now has {leaderboard[giver_id]['points']} points.\n"
                   f"{member.display_name} now has {leaderboard[receiver_id]['points']} points.")

@bot.command(name='points')
async def check_points(ctx, member: discord.Member = None):
    """Check points for yourself or another member"""
    if member is None:
        member = ctx.author
    
    leaderboard = load_leaderboard()
    user_id = str(member.id)
    
    if user_id in leaderboard:
        points = leaderboard[user_id]['points']
        await ctx.send(f"{member.mention} has {points} points.")
    else:
        await ctx.send(f"{member.mention} has no points yet.")

@bot.command(name='leaderboard', aliases=['lb'])
async def show_leaderboard(ctx):
    """Show all players in the server ranked by points"""
    leaderboard = load_leaderboard()
    
    if not leaderboard:
        await ctx.send("The leaderboard is empty!")
        return
    
    sorted_users = sorted(leaderboard.items(), key=lambda x: x[1]['points'], reverse=True)
    
    embed = discord.Embed(title="Points Leaderboard", color=discord.Color.blue())

    
    if len(sorted_users) <= 25:
        for i, (user_id, user_data) in enumerate(sorted_users):
            rank = i + 1
            embed.add_field(
                name=f"{rank}. {user_data['name']}",
                value=f"{user_data['points']} points",
                inline=False
            )
        
        await ctx.send(embed=embed)
    else:
        batches = [sorted_users[i:i+25] for i in range(0, len(sorted_users), 25)]
        
        for batch_index, batch in enumerate(batches):
            batch_embed = discord.Embed(
                title=f"Points Leaderboard (Page {batch_index+1}/{len(batches)})",
                color=discord.Color.blue()
            )
            
            for i, (user_id, user_data) in enumerate(batch):
                rank = batch_index * 25 + i + 1
                batch_embed.add_field(
                    name=f"{rank}. {user_data['name']}",
                    value=f"{user_data['points']} points",
                    inline=False
                )
            
            await ctx.send(embed=embed)

@bot.command(name='resetleaderboard')
@commands.has_permissions(administrator=True)
async def reset_leaderboard(ctx):
    """Reset the entire leaderboard (Admin only)"""
    confirmation_message = await ctx.send("⚠️ Are you sure you want to reset the entire leaderboard? This cannot be undone. React with ✅ to confirm.")
    await confirmation_message.add_reaction("✅")
    
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == confirmation_message.id
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        save_leaderboard({})
        await ctx.send("🗑️ Leaderboard has been reset.")
    except TimeoutError:
        await ctx.send("Leaderboard reset cancelled.")

bot.run('bot_token')