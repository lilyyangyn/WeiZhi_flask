# -*- coding: UTF-8 -*-     
#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand 
from app.models import User, Dish, Restaurant, Spot, Order, Deposit

COV = None
if os.environ.get('TEST_COVERAGE'):
	import coverage
	COV = coverage.coverage(branch=True, include='app/*')
	COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 基本命令行选项: shell - 在程序的上下文中启动Python shell会话
#								runserver - 启动Web服务器
manager = Manager(app)

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Dish=Dish, Restaurant=Restaurant, 
							Spot=Spot, Order=Order, Deposit=Deposit)
# 注册回调函数使shell自动导入数据库实例及模型，避免每次启动shell时重复手动导入
manager.add_command("shell", Shell(make_context=make_shell_context)) 

# 导出数据库迁移命令, 附加到Flask- Script的manager对象上。 
# 常用命令: init, upgrade, downgrade
# 	revision 手动创建迁移; migrate 自动创建迁移
manager.add_command('db', MigrateCommand)

@manager.command
def test(coverage=False):
	# add command 'test' for unit tests
	# use '--coverage' to start coverage test
	if coverage and not os.environ.get('TEST_COVERAGE'):
		import sys
		os.environ['TEST_COVERAGE'] = '1'
		# restart the shell to guarantee accuracy
		os.execvp(sys.executable, [sys.executable] + sys.argv)
	print('"""Run the unit tests."""')
	import unittest
 	tests = unittest.TestLoader().discover('tests')
 	unittest.TextTestRunner(verbosity=2).run(tests)
 	# generate coverage test
 	if COV:
 		COV.stop()
 		COV.save()
 		print('Coverage Summary:')
 		COV.report()
 		basedir = os.path.abspath(os.path.dirname(__file__))
 		covdir = os.path.join(basedir, 'tmp/coverage')
 		COV.html_report(directory=covdir)
 		print('HTML version: file://%s/index.html' % covdir)
 		COV.erase() 


if __name__ == '__main__':
    manager.run()