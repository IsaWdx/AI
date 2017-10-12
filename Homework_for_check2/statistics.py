filenames = ["ab.txt", "minimax.txt"]
for name in filenames:
    f = open(name)
    pre_ave_fac, ave_fac = 0, 0
    pre_total, total = 0, 0
    pre_hit, hit = 0, 0

    for line in f:

        if line.strip() == "FINAL BOARD":
            ave_fac += pre_ave_fac

            total += pre_total
            hit += pre_hit

        t = line.strip().split("=")

        if len(t) == 1:
            continue
        elif len(t) == 2:
            pre_ave_fac = float(t[1].strip())
        elif len(t) == 3:
            pre_total = int(t[1].strip().split()[0])
            pre_hit = float(t[2].strip())


    ave_fac /= 30.0
    total /= 30.0
    hit /= 30.0
    print (ave_fac, total, hit)






        
	
