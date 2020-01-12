# -*- coding: UTF-8 -*-     
#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand 
from app.models import User, Dish, Restaurant, Spot, Order, Deposit

app = create_app('development')
# 基本命令行选项: shell - 在程序的上下文中启动Python shell会话
#								runserver - 启动Web服务器
manager = Manager(app)

migrate = Migrate(app, db)
# 导出数据库迁移命令, 附加到Flask- Script的manager对象上。 
# 常用命令: init, upgrade, downgrade
# 	revision 手动创建迁移; migrate 自动创建迁移
manager.add_command('db', MigrateCommand)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Dish=Dish, Restaurant=Restaurant, 
							Spot=Spot, Order=Order, Deposit=Deposit)
# 注册回调函数使shell自动导入数据库实例及模型，避免每次启动shell时重复手动导入
manager.add_command("shell", Shell(make_context=make_shell_context)) 

if __name__ == '__main__':
    manager.run()