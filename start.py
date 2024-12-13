import time

import pgzrun  # 导入游戏库
import random  # 导入随机库
import pygame  # 导入 pygame 库
import pymunk
import pymunk.pygame_util
from pgzero.actor import Actor
import math
import os

SCORE_FILE = "score_record.txt"  # 保存分数的文件路径
if os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "r") as file:
        try:
            Record = int(file.read().strip())
        except ValueError:
            Record = 0
else:
    Record = 0
def save_score(score):
    """保存最高分到文件"""
    with open(SCORE_FILE, "w") as file:
        file.write(str(score))
total_score=0
man_health = 10  # 人物初始血量
man_max_health = 10  # 最大血量
platform_health = 10  # 平台初始血量

laser_active = False  # 激光是否激活
laser_display_timer = 0  # 激光显示计时器
LASER_DISPLAY_TIME = 60  # 激光显示时间（帧数，例如 60 帧约为 1 秒）
explode_display_timer=0
EXPLODE_DISPLAY_TIME = 60
laser_actor = None  # 激光 Actor
explode_visible=False
explode=None

current_tool = None  # 当前道具类型
tool_used = False  # 道具是否已被使用

monster_speed_multiplier=0

# for i in range(4):
#     original_image = pygame.image.load(f"images/zombie_{i}.png")  # 加载原始图片
#     scaled_image = pygame.transform.scale(original_image, (50, 50))  # 缩放到 50x50
#     pygame.image.save(scaled_image, f"images/zombie_scaled_{i}.png")  # 保存缩小后的图片
#


# 设置窗口大小和标题
WIDTH = 480
HEIGHT = 700
TITLE = '动感按钮示例'

state = pygame.transform.scale(pygame.image.load("images/state.png"), (WIDTH//6.7, HEIGHT//3.7))
pygame.image.save(state, f"images/state.png")

# 加载并缩放背景图片
start_background = pygame.transform.scale(pygame.image.load("images/start_background.png"), (WIDTH, HEIGHT))  # 初始背景
background_1 = pygame.transform.scale(pygame.image.load("images/background_2.png"), (WIDTH, HEIGHT))
background_3 = pygame.transform.scale(pygame.image.load("images/background_3.png"), (WIDTH, HEIGHT))


current_background = start_background  # 当前背景，初始为 `start_background`

# 初始化按钮
finish_positions = [
    (WIDTH // 3, HEIGHT // 5),
    (WIDTH * 2 // 3, HEIGHT * 2 // 5),
    (WIDTH // 3, HEIGHT * 3 // 5),
    (WIDTH * 2 // 3, HEIGHT * 4 // 5)
]

button = Actor('start_no')  # 初始加载为“start_no”图片
button.pos = WIDTH // 2, HEIGHT // 2 + 100  # 设置按钮位置

man = Actor('man_scaled', pos=(WIDTH // 4 - 20, HEIGHT // 5 - 30))  # 创建 man
man_visible = False  # 控制 man 图片是否可见
hand = Actor('hand_scaled', pos=(WIDTH // 2, HEIGHT // 3 - 20))  # 创建 hand
tool=Actor('tool', pos=(WIDTH // 2+60, HEIGHT *2// 3+20))
state=Actor('state', pos=(WIDTH - 34, HEIGHT // 2-23))

# Pymunk 空间初始化
space = pymunk.Space()
space.gravity = (0, 900)  # 设置重力向下

# 初始化斜坡
slope_start = (70, 630)
slope_end = (195, 670)
slope_body = pymunk.Body(body_type=pymunk.Body.STATIC)
slope_shape = pymunk.Segment(slope_body, slope_start, slope_end, 2)
slope_shape.elasticity = 0.5
slope_shape.friction = 0.5


space.add(slope_body, slope_shape)


#第二个斜坡
slope_start_2 = (410, slope_start[1])
slope_end_2 = (285, slope_end[1])

# 初始化第二个对称斜坡
slope_body_2 = pymunk.Body(body_type=pymunk.Body.STATIC)
slope_shape_2 = pymunk.Segment(slope_body_2, slope_start_2, slope_end_2, 2)
slope_shape_2.elasticity = 0.5
slope_shape_2.friction = 0.5
space.add(slope_body_2, slope_shape_2)

wall_start_1 = (70,630)
wall_end_1=(70,200)
wall_body_1= pymunk.Body(body_type=pymunk.Body.STATIC)
wall_shape_1=pymunk.Segment(wall_body_1, wall_start_1, wall_end_1, 2)
wall_shape_1.elasticity = 0.5
wall_shape_1.friction = 0.5
space.add(wall_body_1, wall_shape_1)

wall_start_2 = (410,630)
wall_end_2=(410,200)
wall_body_2= pymunk.Body(body_type=pymunk.Body.STATIC)
wall_shape_2=pymunk.Segment(wall_body_2, wall_start_2, wall_end_2, 2)
wall_shape_2.elasticity = 0.5
wall_shape_2.friction = 0.5
space.add(wall_body_2, wall_shape_2)

wall_start_3 = (205,329)
wall_end_3=(205,537)
wall_body_3= pymunk.Body(body_type=pymunk.Body.STATIC)
wall_shape_3=pymunk.Segment(wall_body_3, wall_start_3, wall_end_3, 2)
wall_shape_3.elasticity = 0.5
wall_shape_3.friction = 0.5
space.add(wall_body_3, wall_shape_3)

wall_start_4 = (343,373)
wall_end_4=(343,413)
wall_body_4= pymunk.Body(body_type=pymunk.Body.STATIC)
wall_shape_4=pymunk.Segment(wall_body_4, wall_start_4, wall_end_4, 2)
wall_shape_4.elasticity = 0.5
wall_shape_4.friction = 0.5
space.add(wall_body_4, wall_shape_4)


wall_start_5 = (343,477)
wall_end_5=(343,517)
wall_body_5= pymunk.Body(body_type=pymunk.Body.STATIC)
wall_shape_5=pymunk.Segment(wall_body_5, wall_start_5, wall_end_5, 2)
wall_shape_5.elasticity = 0.5
wall_shape_5.friction = 0.5
space.add(wall_body_5, wall_shape_5)

wall_start_5 = (WIDTH//2+18,496)
wall_end_5=(WIDTH//2+70,545)
wall_body_5= pymunk.Body(body_type=pymunk.Body.STATIC)
wall_shape_5=pymunk.Segment(wall_body_5, wall_start_5, wall_end_5, 2)
wall_shape_5.elasticity = 0.5
wall_shape_5.friction = 0.5
space.add(wall_body_5, wall_shape_5)

# 添加屏幕中央的圆形
circle_radius_1 = 23  # 圆的半径
circle_mass = 5  # 圆的质量

# 创建物理刚体
# 创建静态刚体
circle_body = pymunk.Body(body_type=pymunk.Body.STATIC)
circle_body.position = (WIDTH // 2+32, HEIGHT // 2+56)  # 设置圆的位置
# 创建物理形状
circle_shape = pymunk.Circle(circle_body, circle_radius_1)
circle_shape.elasticity = 0.8 # 设置弹性
circle_shape.friction = 0.5  # 设置摩擦力
# 将圆添加到物理空间
space.add(circle_body, circle_shape)


circle_radius_2 = 11  # 圆的半径
circle_body_2 = pymunk.Body(body_type=pymunk.Body.STATIC)
circle_body_2.position = (WIDTH // 2+70, HEIGHT // 2-15)  # 设置圆的位置
# 创建物理形状
circle_shape_2 = pymunk.Circle(circle_body_2, circle_radius_2)
# 将圆添加到物理空间
space.add(circle_body_2, circle_shape_2)

circle_radius_3 = 10  # 圆的半径
circle_body_3= pymunk.Body(body_type=pymunk.Body.STATIC)
circle_body_3.position = (WIDTH // 2+22, HEIGHT // 3+57)  # 设置圆的位置
# 创建物理形状
circle_shape_3 = pymunk.Circle(circle_body_3, circle_radius_3)
# 将圆添加到物理空间
space.add(circle_body_3, circle_shape_3)

double_zone_x_start = WIDTH // 2 + 100  # 区域的左边界
double_zone_x_end = WIDTH // 2 + 200  # 区域的右边界
double_zone_y_min = 400 - 10  # 区域的上边界
double_zone_y_max = 400 + 10  # 区域的下边界

triple_zone_x_start = WIDTH // 2 + 100  # 区域的左边界
triple_zone_x_end = WIDTH // 2 + 200  # 区域的右边界
triple_zone_y_min = 500- 10  # 区域的上边界
triple_zone_y_max = 500 + 10  # 区域的下边界

multiply_zone_x_start = WIDTH // 4-50  # 区域左边界
multiply_zone_x_end = WIDTH // 4 + 87  # 区域右边界
multiply_zone_y = HEIGHT // 2+120  # 区域的固定 y 值

# 已经处理过的子弹列表，避免重复处理
bullets_multiplied = []

tool_visible = True  # 道具是否可见
cooldown_timer = 0  # 道具冷却计时器
COOLDOWN_TIME = 1200  # 冷却时间（帧数，20 秒）
reward_display = None  # 显示的奖励
reward_timer = 0  # 奖励显示计时器

# 子弹列表
bullets = []
bullet_timer = 0  # 用于生成子弹的计时器

# 倒计时相关
countdown_sequence = ["","3", "2", "1", "Start!"]  # 倒计时文字序列
countdown_visible = False
countdown_index = 0
countdown_timer = 0
countdown_text = ""

# 控制逻辑变量
hovering = False
mouse_position = (0, 0)  # 初始鼠标位置
button_visible = True  # 主按钮是否可见
main_button_clicked = False  # 主按钮是否被点击的标志
secondary_buttons_visible = True  # 次按钮是否可见（是否显示 n_start 按钮）

# 人物和 hand 移动变量
man_speed = 2
hand_speed = 3
moving_up = False
moving_down = False
moving_left = False
moving_right = False
collected_bullets =0

game_over = False  # 游戏结束标志
game_over_image = Actor('game_over', center=(WIDTH // 2, HEIGHT // 2))  # 加载 Game Over 图片

back_button = Actor('back', center=(WIDTH // 2, HEIGHT // 2 + 100))  # 创建返回按钮的位置
back_button_visible = False  # 控制返回按钮的显示

# 加载调试工具
draw_options = pymunk.pygame_util.DrawOptions(None)  # 调试绘制需要动态传递 screen


platform_exists = True  # 平台是否存在的标志
platform_body = None  # 平台的物理刚体
platform_shape = None  # 平台的物理形状
platform_y = multiply_zone_y - 97  # 平台的 Y 坐标




monsters = []  # 每个怪物存储为字典，包含其 Actor、图片索引和速度
def spawn_monster():
    """生成一个新的怪物"""
    global monster_speed_multiplier
    monster_speed_multiplier-=0.001
    # 随机生成怪物的初始位置
    x = int(WIDTH * 8 / 9)  # 横坐标
    y = random.randint(50, 160)  # 纵坐标

    # 缩放怪物图片
    scaled_image = pygame.transform.scale(pygame.image.load("images/zombie_0.png"), (50, 50))  # 缩小到 50x50 大小
    pygame.image.save(scaled_image, "images/zombie_scaled_0.png")  # 保存缩小后的图片

    # 创建怪物 Actor，使用缩放后的图片
    monster_actor = Actor('zombie_scaled_0', pos=(x, y))  # 使用缩小后的图片

    # 将怪物添加到列表中，初始图片索引为 0，速度为 -5（向左移动）
    monsters.append({'actor': monster_actor, 'image_index': 0, 'speed': -0.3+monster_speed_multiplier})


def update_monsters():
    """更新怪物逻辑，包括动画和移动"""
    for monster in monsters[:]:  # 遍历所有怪物
        if "frame_timer" not in monster:
            monster["frame_timer"] = 0  # 初始化计时器

        monster["frame_timer"] += 1
        if monster["frame_timer"] >= 5:  # 每 10 帧切换一次图片
            monster['image_index'] = (monster['image_index'] + 1) % 4  # 图片索引 0-3 循环
            monster['actor'].image = f'zombie_scaled_{monster["image_index"]}'  # 切换图片
            monster["frame_timer"] = 0  # 重置计时器

        # 更新怪物位置
        monster['actor'].x += monster['speed']  # 怪物向左移动

        # 如果怪物超出屏幕范围，则移除
        if monster['actor'].x < -50:  # 超出屏幕左边界
            monsters.remove(monster)



manual_bullets = []  # 每个子弹存储为一个字典：{'actor': Actor, 'speed': int}
def spawn_bullet():
    """生成新的子弹"""
    width = 25  # 矩形子弹的宽度
    height = 15  # 矩形子弹的高度
    mass = 1  # 子弹的质量

    # 计算矩形的惯性矩
    inertia = pymunk.moment_for_box(mass, (width, height))

    # 创建子弹刚体
    bullet_body = pymunk.Body(mass, inertia)
    bullet_body.position = (hand.x+20, hand.y + 20)  # 子弹初始位置

    # 创建矩形形状
    bullet_shape = pymunk.Poly.create_box(bullet_body, (width, height))
    bullet_shape.elasticity = 0.8  # 碰撞的弹性
    bullet_shape.friction = 0.5  # 碰撞的摩擦力

    # 创建子弹图片的 Actor
    bullet_actor = Actor('bullet_scaled', pos=bullet_body.position)

    # 添加到物理空间
    space.add(bullet_body, bullet_shape)

    # 添加到子弹列表，便于更新和绘制
    bullets.append((bullet_body, bullet_shape, bullet_actor))


def spawn_manual_bullet():
    """
    从人物 man 位置发射子弹
    direction: tuple(dx, dy)，表示子弹的移动方向
    """
    global collected_bullets

    if collected_bullets > 0:  # 确保有足够的子弹可以发射
        # 创建子弹 Actor
        bullet_actor = Actor('bullet_scaled_right')
        bullet_actor.pos = (man.x + 10, man.y)  #

        # 将子弹添加到手动发射的子弹列表中
        manual_bullets.append({'actor': bullet_actor,'speed':5})  # 使用 direction 控制移动

        # 减少收集到的子弹数量
        collected_bullets -= 1


def update_manual_bullets():
    """更新手动发射的子弹，包括炸弹逻辑"""
    global monsters,explode_visible,explode,total_score
    for bullet in manual_bullets[:]:
        bullet['actor'].x += bullet['speed']  # 更新子弹的水平位置

        # 检测子弹与怪物的碰撞
        for monster in monsters[:]:
            if bullet['actor'].colliderect(monster['actor']):
                if bullet.get('type') == 'bomb':  # 如果是炸弹
                    explode = Actor('explode', pos=(bullet['actor'].x, bullet['actor'].y))
                    explode_visible = True
                    # 检测范围内的敌人
                    to_remove = []  # 存储需要移除的敌人
                    for m in monsters:
                        distance = math.sqrt(
                            (m['actor'].x - bullet['actor'].x) ** 2 + (m['actor'].y - bullet['actor'].y) ** 2)
                        if distance < 150:  # 设置炸弹范围
                            to_remove.append(m)

                    # 移除范围内的敌人
                    for m in to_remove:
                        total_score += 1
                        # print(total_score)
                        if m in monsters:  # 确保敌人在列表中
                            monsters.remove(m)

                # 移除炸弹或子弹
                if bullet in manual_bullets:
                    total_score += 1
                    print(total_score)
                    manual_bullets.remove(bullet)
                if monster in monsters:  # 确保敌人在列表中
                    monsters.remove(monster)
                break  # 子弹或炸弹已移除，无需再检测其他怪物

        # 如果子弹或炸弹超出屏幕范围，则移除
        if bullet['actor'].x > WIDTH:
            manual_bullets.remove(bullet)


def update():
    global bullet_timer, countdown_timer, countdown_index, countdown_visible, countdown_text, man_visible, man_health, game_over, collected_bullets, back_button_visible
    global double_zone_x_start,double_zone_y_start,double_zone_x_end,double_zone_y_end
    global triple_zone_x_start, triple_zone_y_start, triple_zone_x_end, triple_zone_y_end
    global platform_exists, platform_health, current_background
    global tool_visible, cooldown_timer, reward_display, reward_timer
    global laser_active, laser_display_timer
    global explode_display_timer,explode_visible
    if game_over:
        back_button_visible = True  # 游戏结束时显示返回按钮
        return  # 如果游戏结束，不再更新游戏逻辑

    if button_visible:  # 检测鼠标是否悬停在按钮上
        check_button(mouse_position)
    elif countdown_visible:  # 倒计时逻辑
        countdown_timer -= 1
        if countdown_timer <= 0:
            countdown_index += 1
            if countdown_index < len(countdown_sequence):
                countdown_text = countdown_sequence[countdown_index]
                countdown_timer = 60  # 每个文字显示 1 秒
            else:
                countdown_visible = False  # 倒计时结束
                man_visible = True  # 显示人物

    # 倒计时结束后，生成怪物
    if man_visible:
        if platform_exists and platform_body is None:  # 如果平台需要存在且未初始化
            create_platform()
        if random.randint(1, 50) == 1:  # 每帧有概率生成一个怪物（控制生成频率）
            spawn_monster()

        # 检测怪物是否到达人物的 x 坐标
        for monster in monsters[:]:
            if abs(monster['actor'].x - man.x) < 10:  # 怪物和人物的 x 坐标接近
                monsters.remove(monster)  # 移除怪物
                man_health -= 1  # 人物扣血
                if man_health <= 0:
                    man_health = 0  # 确保血量不低于 0
                    game_over = True  # 游戏结束
    if laser_active:
        if laser_display_timer > 0:
            laser_display_timer -= 1
        else:
            laser_active = False  # 关闭激光显示
    if explode_visible:
        if explode_display_timer > 0:
            explode_display_timer -= 1
        else:
            explode_visible = False  # 关闭激光显示


    # 更新人物移动逻辑
    if moving_up:
        man.y = max(50, man.y - man_speed)
    if moving_down:
        man.y = min(HEIGHT // 4 - 15, man.y + man_speed)

    # 更新 hand 的移动逻辑
    if moving_left:
        hand.x = max(80, hand.x - hand_speed)
    if moving_right:
        hand.x = min(WIDTH - 100, hand.x + hand_speed)

    # 更新手动发射的子弹并检测碰撞
    update_manual_bullets()

    # 更新怪物
    update_monsters()

    update_rewards()

    # 子弹生成逻辑
    bullet_timer += 1
    if bullet_timer >= 180:
        spawn_bullet()
        bullet_timer = 0

    # 更新物理空间
    space.step(1 / 80.0)

    # 移除超出屏幕的自动生成的子弹
    # 子弹翻倍区域定义

    # 用于记录已经翻倍的子弹，避免重复翻倍
    bullets_doubled = []
    bullets_tripled=[]

    # 水平偏移量
    offset_x = 15  # 偏移的距离，表示新子弹位于当前子弹的右侧
    num_double=0
    num_triple=0
    current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
    last_multiply_time = [0]  # 记录每个子弹上次倍增的时间
    multy_time=0
    # 更新自动生成的子弹
    for bullet_body, bullet_shape, bullet_actor in bullets[:]:
        bullet_actor.pos = bullet_body.position  # 同步图片位置

        # 获取子弹的顶端 y 坐标
        bullet_top_y = bullet_body.position.y+2
        velocity=math.sqrt(bullet_body.velocity.x**2 + bullet_body.velocity.y**2)

        bullet_actor.pos = bullet_body.position

        # 检测子弹与道具的碰撞
        if tool_visible and bullet_actor.colliderect(tool):
            tool_visible = False
            cooldown_timer = COOLDOWN_TIME
            space.remove(bullet_body, bullet_shape)
            bullets.remove((bullet_body, bullet_shape, bullet_actor))
            trigger_random_reward()


        # 检查子弹是否进入+1区域
        if (
                double_zone_x_start <= bullet_body.position.x <= double_zone_x_end and
                double_zone_y_max-velocity/200<=bullet_top_y <= double_zone_y_max+velocity/200 and
                (bullet_body,num_double) not in bullets_doubled
        ):
            # 标记该子弹为已+1
            num_double+=1
            bullets_doubled.append((bullet_body,num_double))
            # print("already add current bullet")
            # print(bullet_body)

            # 创建翻倍的子弹
            new_bullet_body = pymunk.Body(bullet_body.mass, bullet_body.moment)
            new_bullet_body.position = (bullet_body.position.x - offset_x, bullet_body.position.y)  # 在右侧生成子弹
            new_bullet_body.velocity = bullet_body.velocity  # 保持与原子弹相同的速度

            new_bullet_shape = pymunk.Poly.create_box(new_bullet_body, (29, 19))
            new_bullet_shape.elasticity = bullet_shape.elasticity
            new_bullet_shape.friction = bullet_shape.friction

            new_bullet_actor = Actor('bullet_scaled', pos=new_bullet_body.position)

            # 添加新子弹到物理空间和子弹列表
            space.add(new_bullet_body, new_bullet_shape)
            bullets.append((new_bullet_body, new_bullet_shape, new_bullet_actor))
            num_double += 1
            bullets_doubled.append((new_bullet_body,num_double))
            # print("already add new bullet")
        # 检查子弹是否进入+2区域


        # print(velocity)
        if (
                triple_zone_x_start <= bullet_body.position.x <= triple_zone_x_end and
                triple_zone_y_max-velocity/200<=bullet_top_y <= triple_zone_y_max+velocity/200 and
                (bullet_body,num_triple) not in bullets_tripled
        ):
            # print(velocity)
            # 标记该子弹为已+2
            num_triple+=1
            bullets_tripled.append((bullet_body,num_triple))
            # print("already add current bullet3")
            # print(bullet_body)

            # 创建+2的子弹
            new_bullet_body = pymunk.Body(bullet_body.mass, bullet_body.moment)
            new_bullet_body.position = (bullet_body.position.x - offset_x, bullet_body.position.y)  # 在右侧生成子弹
            new_bullet_body.velocity = bullet_body.velocity  # 保持与原子弹相同的速度

            new_bullet_shape = pymunk.Poly.create_box(new_bullet_body, (29, 19))
            new_bullet_shape.elasticity = bullet_shape.elasticity
            new_bullet_shape.friction = bullet_shape.friction

            new_bullet_actor = Actor('bullet_scaled', pos=new_bullet_body.position)

            # 添加新子弹到物理空间和子弹列表
            space.add(new_bullet_body, new_bullet_shape)
            bullets.append((new_bullet_body, new_bullet_shape, new_bullet_actor))
            num_triple += 1
            bullets_tripled.append((new_bullet_body,num_triple))

            #再加一颗子弹
            new_bullet_body = pymunk.Body(bullet_body.mass, bullet_body.moment)
            new_bullet_body.position = (bullet_body.position.x +offset_x, bullet_body.position.y)  # 在右侧生成子弹
            new_bullet_body.velocity = bullet_body.velocity  # 保持与原子弹相同的速度

            new_bullet_shape = pymunk.Poly.create_box(new_bullet_body, (29, 19))
            new_bullet_shape.elasticity = bullet_shape.elasticity
            new_bullet_shape.friction = bullet_shape.friction

            new_bullet_actor = Actor('bullet_scaled', pos=new_bullet_body.position)

            # 添加新子弹到物理空间和子弹列表
            space.add(new_bullet_body, new_bullet_shape)
            bullets.append((new_bullet_body, new_bullet_shape, new_bullet_actor))
            num_triple += 1
            bullets_tripled.append((new_bullet_body,num_triple))
            # print("already add new bullet3")

        if (
                multiply_zone_x_start <= bullet_body.position.x <= multiply_zone_x_end
                and abs(bullet_body.position.y - multiply_zone_y) < 5
        ):
            # 检查是否超过冷却时间
            if current_time - last_multiply_time[multy_time] > 1000:  # 冷却 500ms
                last_multiply_time.append(current_time)
                multiply_bullets(bullet_body, bullet_shape)  # 创建新子弹
                multy_time+=1

        # 检测子弹超出屏幕范围并移除

        if (
                platform_exists and  # 平台存在
                multiply_zone_x_start <= bullet_body.position.x <= multiply_zone_x_end and  # 子弹在平台横向范围内
                platform_y - 20 <= bullet_body.position.y <= platform_y + 20  # 子弹触碰平台
        ):
            # 移除子弹
            space.remove(bullet_body, bullet_shape)
            bullets.remove((bullet_body, bullet_shape, bullet_actor))

            # 减少平台血量
            platform_health -= 1
            print(f"Platform health: {platform_health}")  # 调试用

            # 如果平台血量为 0，移除平台
            if platform_health <= 0:
                space.remove(platform_body, platform_shape)  # 从物理空间移除平台
                platform_exists = False  # 标记平台为不存在
                current_background = background_3  # 切换背景图
        if bullet_body.position.y > 670:
            if countdown_index == 5:
                collected_bullets += 1  # 更新收集到的子弹数
            space.remove(bullet_body, bullet_shape)
            bullets.remove((bullet_body, bullet_shape, bullet_actor))


def draw():
    global double_zone_x_start,double_zone_y_min,double_zone_x_end,double_zone_y_max
    global laser_active, laser_actor
    global explode_visible,explode,total_score,Record
    screen.clear()
    screen.blit(current_background, (0, 0))  # 绘制当前背景

    if game_over:
        # 游戏结束时显示 Game Over 图片
        if total_score > Record:
            Record = total_score
            save_score(Record)  # 保存到文件
        game_over_image.draw()
        return  # 退出 draw()，防止其他元素被绘制

    if button_visible:  # 主按钮绘制
        button.draw()
    elif countdown_visible:  # 倒计时文字绘制
        screen.draw.text(
            countdown_text,
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="white",
        )
    if man_visible:  # 绘制 man 和子弹
        man.draw()
        hand.draw()
        tool.draw()
        state.draw()
        # 绘制自动生成的子弹
        for bullet_body, bullet_shape, bullet_actor in bullets:
            bullet_actor.pos = bullet_body.position  # 同步图片位置
            bullet_actor.angle = -math.degrees(bullet_body.angle)
            bullet_actor.draw()  # 使用 Actor 绘制图片

        # 绘制人物发射的子弹
        for bullet in manual_bullets:
            bullet['actor'].draw()  # 绘制子弹

        # 绘制怪物
        for monster in monsters:
            monster['actor'].draw()

        # 绘制血条
        draw_health_bar()
        screen.draw.text(
            f"Record",
            center=(WIDTH - 30, HEIGHT // 2-50),  # 显示在屏幕左上角
            fontsize=25,
            color="green",
        )
        screen.draw.text(
            f"{Record}",
            center=(WIDTH - 30, HEIGHT // 2-30),  # 显示在屏幕左上角
            fontsize=25,
            color="green",
        )
        screen.draw.text(
            f"Score",
            center=(WIDTH-30, HEIGHT//2),  # 显示在屏幕左上角
            fontsize=25,
            color="white",
        )
        screen.draw.text(
            f"{total_score}",
            center=(WIDTH - 30, HEIGHT // 2+20),  # 显示在屏幕左上角
            fontsize=25,
            color="white",
        )

        screen.draw.text(
            f"Bullets: {collected_bullets}",
            topleft=(10, 30),  # 显示在屏幕左上角
            fontsize=30,
            color="white",
        )
        if platform_exists:

            # 绘制平台血量
            screen.draw.text(
                str(platform_health),
                center=(multiply_zone_x_start + (multiply_zone_x_end - multiply_zone_x_start) // 2, platform_y - 20),
                fontsize=30,
                color="white"
            )

        if laser_active and laser_actor:
            laser_actor.draw()  # 绘制激光

        if explode_visible:
            explode.draw()

        if tool_visible:
            tool.draw()
        else:
            screen.draw.text(
                f"Cooldown:"
                f"{cooldown_timer // 60}",
                center=tool.pos,
                fontsize=20,
                color="white",
            )
        if reward_display:
            screen.draw.text(
                reward_display,
                topleft=(110, 10),
                fontsize=30,
                color="black",
            )
            screen.draw.text(
                f"(Press Enter)",
                topleft=(110, 30),
                fontsize=20,
                color="green",
            )

def draw_health_bar():
    """绘制人物血条"""
    bar_width = 100  # 血条的总宽度
    bar_height = 20  # 血条高度
    x = 10  # 血条左上角的 x 坐标
    y = 10  # 血条左上角的 y 坐标

    # 计算当前血量的宽度
    health_width = (man_health / man_max_health) * bar_width

    # 绘制血条背景（灰色）
    screen.draw.filled_rect(Rect((x, y), (bar_width, bar_height)), (100, 100, 100))

    # 绘制当前血量（红色）
    screen.draw.filled_rect(Rect((x, y), (health_width, bar_height)), (255, 0, 0))

    # 绘制血量数字
    screen.draw.text(
        f"Health: {man_health}/{man_max_health}",
        midtop=(x + bar_width // 2, y - 20),
        fontsize=20,
        color="white"
    )



def check_button(mouse_position):
    global hovering
    if button.collidepoint(mouse_position):
        if not hovering:
            button.image = 'start_yes'  # 切换高亮图片
            hovering = True
    else:
        if hovering:
            button.image = 'start_no'  # 恢复默认图片
            hovering = False


def on_mouse_down(pos):
    global button_visible, main_button_clicked, current_background, secondary_buttons_visible, countdown_visible, countdown_timer, countdown_index, back_button_visible, game_over,hovering
    if button_visible and hovering:
        button_visible = False
        main_button_clicked = True
        current_background = background_1
        countdown_visible = True
        countdown_text = countdown_sequence[0]
        countdown_timer = 60  # 每个文字显示 1 秒
        countdown_index = 0  # 初始化倒计时索引



# 修改鼠标移动事件，鼠标悬停到返回按钮时切换图片
def on_mouse_move(pos, rel, buttons):
    global mouse_position
    mouse_position = pos  # 更新鼠标当前位置
    if game_over:  # 如果在游戏结束状态下
        if back_button.collidepoint(pos):
            back_button.image = 'back_click'  # 切换为点击状态图片
        else:
            back_button.image = 'back'  # 恢复为正常状态图片

def on_key_down(key):
    global man, moving_up, moving_down, moving_left, moving_right, tool_used, current_tool, reward_display, reward_timer, collected_bullets
    # print(f"Key pressed: {key}")
    if key == keys.RETURN:  # 检测键名
        # print(f"Key detected. Reward Display: {reward_display}, Tool Used: {tool_used}")
        if reward_display and not tool_used:
            print(f"Using tool: {current_tool}")
            if current_tool == "Laser*1":
                use_laser()
            elif current_tool == "Bomb*1":
                use_bomb()
            elif current_tool == "Bullets+5":
                global collected_bullets
                collected_bullets += 5
            reward_display = None
            tool_used = True

    if key == keys.SPACE:  # 发射普通子弹
        if man_visible:  # 确保人物已可见
            spawn_manual_bullet()  # 发射水平子弹
        man.image = "man_shooting_scaled"  # 切换图片为 `man_shooting`
    if key == keys.UP:
        moving_up = True
    elif key == keys.DOWN:
        moving_down = True
    if key == keys.LEFT:
        moving_left = True
    elif key == keys.RIGHT:
        moving_right = True

def use_laser():
    """发射激光，清除当前水平线上的所有敌人"""
    global monsters, laser_active, laser_display_timer, laser_actor,total_score

    laser_actor = Actor("laser", pos=(man.x + 200, man.y))  # 激光从人物位置发射
    laser_active = True  # 激光激活
    laser_display_timer = LASER_DISPLAY_TIME  # 重置计时器

    # 清除当前水平线上的敌人
    for monster in monsters[:]:
        if abs(monster['actor'].y - man.y) < 30:  # 检测水平线上的敌人
            total_score +=1
            monsters.remove(monster)  # 清除敌人

def use_bomb():
    """发射炸弹，击中敌人后清除范围内的敌人"""
    global explode_display_timer
    global monsters
    bomb_actor = Actor("bomb", pos=(man.x + 10, man.y))  # 炸弹从人物位置发射
    bomb_speed = 5  # 设置炸弹的速度
    explode_display_timer = EXPLODE_DISPLAY_TIME
    manual_bullets.append({'actor': bomb_actor, 'speed': bomb_speed, 'type': 'bomb'})  # 将炸弹添加到子弹列表



def on_key_up(key):
    global man, moving_up, moving_down, moving_left, moving_right
    if key == keys.SPACE:  # 检测空格键释放
        man.image = "man_scaled"  # 恢复图片为 `man_scaled`
    if key == keys.UP:
        moving_up = False
    elif key == keys.DOWN:
        moving_down = False
    if key == keys.LEFT:
        moving_left = False
    elif key == keys.RIGHT:
        moving_right = False


def multiply_bullets(original_bullet_body, original_bullet_shape):
    """将子弹数量乘以 10"""
    global bullets
    offset_x = 10  # 新子弹的水平偏移
    offset_y = 10  # 新子弹的垂直偏移

    for i in range(5):  # 创建 10 个新子弹
        new_bullet_body = pymunk.Body(original_bullet_body.mass, original_bullet_body.moment)
        new_bullet_body.position = (
            original_bullet_body.position.x + offset_x * (i % 5),  # 横向排列
            original_bullet_body.position.y + offset_y * (i // 5)  # 纵向排列
        )
        new_bullet_body.velocity = original_bullet_body.velocity  # 保持与原子弹相同的速度

        new_bullet_shape = pymunk.Poly.create_box(new_bullet_body, (29, 19))
        new_bullet_shape.elasticity = original_bullet_shape.elasticity
        new_bullet_shape.friction = original_bullet_shape.friction

        new_bullet_actor = Actor('bullet_scaled', pos=new_bullet_body.position)

        # 添加到物理空间和子弹列表
        space.add(new_bullet_body, new_bullet_shape)
        bullets.append((new_bullet_body, new_bullet_shape, new_bullet_actor))

def visualize_multiply_zone():
    """可视化子弹倍增的区域"""
    # 绘制倍增区域
    multiply_zone_rect = Rect(
        (multiply_zone_x_start, multiply_zone_y - 5),
        (multiply_zone_x_end - multiply_zone_x_start, 10)  # 高度为 10
    )
    screen.draw.filled_rect(multiply_zone_rect, (0, 255, 0))  # 使用绿色填充矩形


def create_platform():
    """创建物理平台"""
    global platform_body, platform_shape

    if not platform_exists:  # 如果平台标记为不存在，不执行创建
        return

    platform_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # 静态刚体
    platform_shape = pymunk.Segment(
        platform_body,
        (multiply_zone_x_start, platform_y),
        (multiply_zone_x_end, platform_y),
        5  # 平台的厚度
    )
    platform_shape.elasticity = 0.5  # 弹性
    platform_shape.friction = 0.5  # 摩擦力
    space.add(platform_body, platform_shape)  # 添加到物理空间

def trigger_random_reward():
    """生成随机奖励并重置状态"""
    global reward_display, reward_timer, current_tool, tool_used
    rewards = ["Laser*1", "Bomb*1", "Bullets+5"]
    current_tool = random.choice(rewards)  # 随机选择道具
    # current_tool="Bomb*1"
    reward_display = current_tool
    reward_timer = 600  # 显示时间（帧数，10 秒）
    tool_used = False  # 道具未被使用
    print(reward_display, reward_timer, current_tool, tool_used)


def update_rewards():
    """更新奖励计时和状态"""
    global cooldown_timer, tool_visible, reward_timer, reward_display
    if cooldown_timer > 0:
        cooldown_timer -= 1
        if cooldown_timer == 0:
            tool_visible = True
    if reward_timer > 0:
        reward_timer -= 1
        if reward_timer == 0:
            reward_display = None  # 超时后清除显示
            current_tool = None  # 道具失效


# 开始运行游戏


pgzrun.go()
