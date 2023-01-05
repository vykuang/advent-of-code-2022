#! /usr/bin/env python
"""
AoC 2022 Day
"""
from functools import reduce
import sys
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def load_input(fp):
    with open(fp) as f_in:
        for line in f_in.read().splitlines():
            yield line

class Monkey:
    def __init__(self, label: int, items: list[int], worry_op: list, toss_test: list, rec_a: int, rec_b: int):
        self.label = label
        if items:
            self.items = items
        else:
            self.items = []
        self.worry_op = self.parse_worry_op(worry_op=worry_op)
        self.toss_test = self.parse_toss_test(toss_test=toss_test)
        self.recvs = [rec_b, rec_a]
        self.item_count = 0

    def parse_worry_op(self, worry_op):
        logger.debug(f"parse_worry_op input: {worry_op}")
        op, arg = worry_op[-2:]
        if arg.isdigit():
            arg = int(arg)
        else:
            return lambda x: int((x ** 2) / 3)
        match op:
            case '+':
                return lambda x: int((x + arg) / 3)
            case '-':
                return lambda x: int((x - arg) / 3)
            case '/':
                return lambda x: int(x / arg / 3)
            case '*':
                return lambda x: int(x * arg / 3)
                
    def parse_toss_test(self, toss_test):
        div_test = int(toss_test[-1])
        return lambda x: not(bool(x % div_test))


    def toss_item(self):
        logger.debug(f"monkey {self.label}")
        logger.debug(f"old items: {self.items}")
        new_items = [self.worry_op(item) for item in self.items]
        rec = [self.recvs[self.toss_test(item)] for item in new_items]
        toss_dict = defaultdict(list)
        for monkey, item in zip(rec, new_items):
            toss_dict[monkey].append(item)
        # all items have been tossed
        self.items.clear()    
        for rec in toss_dict:
            logger.debug(f"monkey {rec} will receive {toss_dict[rec]}")
        self.item_count += len(new_items)
        return toss_dict

if __name__ == "__main__":

    fn = sys.argv[1]
    match fn:
        case "test" | "input":
            fp = f"{fn}.txt"
            test = fn == "test" 
        case _:
            raise ValueError(f"{fn} cannot be used")
            
    if test:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
    else:
        logger.setLevel(logging.INFO)
    
#     monkeys = []
    monkeys = defaultdict(Monkey)
    for line in load_input(fp):
        logger.debug(f"line: {line}")
        logger.debug(f"split line: {line.split()}")
        match line.split():
            case ["Monkey", monkey_id]:
                # start of new monkey; get next 5 lines
                monkey_id = int(monkey_id[:-1])
                logger.debug(f"monkey: {monkey_id}")
            case ["Starting", *items]:
                logger.debug(f"items: {items}")
                worries = [int(worry) for item in items if (worry := item.replace(',', '')).isnumeric()]
                logger.debug(f"initial worries: {worries}")
            case ["Operation:", *worry_op]:
                logger.debug(worry_op)
            case ["Test:", *toss_test]:
                logger.debug(f"toss_test: {toss_test}")
            case ["If", "true:", *rec_a]:
                rec_a = int(rec_a[-1])
                logger.debug(f"rec_a: monkey {rec_a}")
            case ["If", "false:", *rec_b]:
                rec_b = int(rec_b[-1])
                logger.debug(f"rec_b: monkey {rec_b}")
                logger.debug(f"monkey_id: {monkey_id}")
                monkeys[monkey_id] = Monkey(label=monkey_id, 
                                    items=worries, 
                                    worry_op=worry_op,
                                    toss_test=toss_test, 
                                    rec_a=rec_a, 
                                    rec_b=rec_b)
            case []:
                logger.debug("blank line detected")
    logger.debug(f"monkeys recorded: {len(monkeys)}")
    for _ in range(20):
        for i in range(len(monkeys)):
            items_tossed = monkeys[i].toss_item()
            for monkey in items_tossed:
                monkeys[monkey].items.extend(items_tossed[monkey])

    item_counts = sorted([monkeys[label].item_count for label in monkeys], reverse=True)
    lim = 2
    biz = reduce(lambda x, y: x * y, item_counts[:lim])
    print(f'monkey biz: {biz}')
