import os
import click
from flask.cli import with_appcontext
from dotenv import load_dotenv, set_key
from models import db, User, MenuItem, TableDefinition

def register_commands(app):
    """ 注册自定义命令 """
    app.cli.add_command(init_db_command)
    app.cli.add_command(config_db_command)
    app.cli.add_command(seed_db_command)

@click.command('db-init')
@with_appcontext
def init_db_command():
    """ 创建数据库表 """
    create_tables()
    click.echo('数据表创建成功。')

@click.command('db-config')
@click.argument('db_type', type=click.Choice(['sqlite', 'mysql']))
@with_appcontext
def config_db_command(db_type):
    """ 配置数据库类型 """
    # 更新.env文件以选择数据库类型
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write(f"DATABASE_TYPE={db_type}\n")
    else:
        # 读取.env文件
        load_dotenv(env_path)
        # 设置数据库类型
        set_key(env_path, 'DATABASE_TYPE', db_type)
    
    click.echo(f'数据库类型为 {db_type}。')
    click.echo('可能需要重启服务才能生效。')

@click.command('db-seed')
@with_appcontext
def seed_db_command():
    """ 创建管理员用户和表格管理菜单，并填充初始数据。"""
    
    # 创建管理员用户
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', password='admin123')
        db.session.add(admin)
        
    # 创建表格管理菜单
    if not MenuItem.query.filter_by(name='tables').first():
        # 创建表格管理菜单
        tables_menu = MenuItem(
            name='tables',
            display_name='表格',
            path='/tables',
            icon='table',
            order=1
        )
        
        settings_menu = MenuItem(
            name='settings',
            display_name='设置',
            path='/settings',
            icon='settings',
            order=2
        )
        
        db.session.add(tables_menu)
        db.session.add(settings_menu)
        
        # 创建表格管理子菜单
        table_mgmt = MenuItem(
            name='table-management',
            display_name='表格管理',
            path='/settings/table-management',
            icon='edit',
            order=1,
            parent=settings_menu
        )
        
        db.session.add(table_mgmt)
    
    db.session.commit()
    click.echo('数据库已填充初始数据。')

def create_tables():
    """ 创建所有数据库表 """
    db.create_all()
    click.echo('所有数据表创建成功。') 