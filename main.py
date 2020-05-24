from Generation import TaskGen
from non_rt_gen_main import *
from ga_main import *
from hrt_main import *
from DFGA import *
import test_out_csv

test_out_csv.init()
TaskGen().gen_task()
non_rt_gen()
# dfga_run()
hrt_run()


