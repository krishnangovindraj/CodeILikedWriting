from problog.program import PrologFile
from ts_lhm import ThetaSubsumptionLHM

TEST_FACTORIZER_BG = "factorize.bg"


def main():

    bg = PrologFile(TEST_FACTORIZER_BG)
    tslhm = ThetaSubsumptionLHM(None, None, bg)
    tslhm.setup()

    # print(tslhm.bg_groundings)
    # print(tslhm.rules)
    # print(tslhm.affected_list
    
    pending_groundings = set()
    for tsig in tslhm.bg_groundings:
        pending_groundings.update(tslhm.bg_groundings[tsig])

    all_groundings = set(pending_groundings)


    derived_groundings = set()
    while len(pending_groundings) > 0:      # You're not seeing double.
        while len(pending_groundings) > 0:
            t = pending_groundings.pop()
            ng = tslhm.propagate_new_knowledge(t)
            derived_groundings.update(ng)
            
        newly_derived = derived_groundings - all_groundings
        # print("Newly derived: " + str(newly_derived))
        all_groundings.update(newly_derived)        
        pending_groundings = newly_derived
        derived_groundings = set()
    
    # print()
    print(all_groundings)


if __name__=="__main__":
    main()