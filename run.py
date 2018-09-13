from proxypool.scheduler import Scheduler
import sys
import io

# 修改标准输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main() # 失败就再次调用


if __name__ == '__main__':
    main()
