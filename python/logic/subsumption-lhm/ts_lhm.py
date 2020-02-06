
from problog.logic import Term, Var, Constant, Clause
from problog.program import SimpleProgram

from pyswip import Prolog as pyswip_Prolog

"""Assumption - No logic stuff happens. Only relational stuff. i.e., not facts with variables.
divides(A,A). should not be in the bg. 
divides(A,A):- num(A). would be ok, provided that num(A) are ground facts.
All terms are ground. 
"""
_HAX_SUBTLE_PATH = "./subtle-wrapper.pl"


def multidict_safe_add(d, k, v, default_type=set):
    if k not in d:
        d[k] = default_type()
    d[k].add(v)


class RuleInstance:
    def __init__(self, clause):
        self._clause = clause   # For debugging for now
        self.head = clause.head
        self.body = RuleInstance.flatten_body(clause.body) 


    @staticmethod 
    def flatten_body(body):
        if body.functor == ',':
            bl = list(body.args)
            return  [bl[0]] + RuleInstance.flatten_body(bl[1])
        else:
            return [body]

    def __repr__(self):
        return "RuleInstance:[%s]"%str(self._clause)
        
    def __str__(self):
        return "RuleInstance:[%s]"%str(self._clause)

    def get_body(self):
        return self.body

    def ground_head(self, subst):
        gh = Term(self.head.functor, *self.head.args)
        gh = gh.apply( {k : Constant(subst[k]) for k in subst})
        return gh

class ThetaSubsumptionLHM:

    def __init__(self, prediction_goal, language, bg_program_sp): # 

        self._bg_program_sp = bg_program_sp
        self.prediction_goal = prediction_goal
        self.language = language
        # self.bg_program = None
        self.db = {}

        self.rules = {}         # functor:str -> rule:?
        self.bg_groundings = {}    # functor: str -> list(term:?)
        
        self.affected_list = {}

        self._HAX_SS = set() #  []
        self._HAX_SUBTLE = None

    def setup(self):
        # self._process_language(self.prediction_goal, self.language)
        self._process_bg_program(self._bg_program_sp)
        
        self._HAX_SUBTLE = pyswip_Prolog()
        self._HAX_SUBTLE.consult(_HAX_SUBTLE_PATH)

    def _process_language(self, prediction_goal, language):
        # When everything is grounded, the modes hardly matter
        pass



    def _process_bg_rule(self, entry):
        rule = RuleInstance(entry)
        body = rule.get_body()
        head_sig = (entry.head.functor, entry.head.arity)
        multidict_safe_add( self.rules, head_sig, rule )
        for b in body:
            multidict_safe_add(self.affected_list, (b.functor, b.arity), rule) # head_sig)


    def _process_bg_program(self, bg_program_sp):
        # This should be in rule_grounder. For now, We piggy back on prolog
        for entry in bg_program_sp:
            if type(entry) == Term:
                multidict_safe_add( self.bg_groundings, (entry.functor, entry.arity), entry)# entry.args)
            elif type(entry) == Clause:
                self._process_bg_rule(entry)
    

    def update_db(self, groundfact):
        self._HAX_SS.add(groundfact) # append(groundfact)

    def fact_in_db(self, groundfact):
        return groundfact in self._HAX_SS

    """ Returns all (grounded) facts entailed by KB ^ groundfact """
    def propagate_new_knowledge(self, groundfact):
        gf_sig = (groundfact.functor, groundfact.arity)
        new_groundings = set()
        __empty_set = set()
        for rule in self.affected_list.get(gf_sig, __empty_set):
            self._propagate_to_rule_and_grind(rule, groundfact, new_groundings)

        self.update_db(groundfact)

        return new_groundings

    @staticmethod
    def new_groundfact_rename(term):
        return Term("newgroundfact__"+ term.functor, term.args)
        # return "newgroundfact__" + term_str # Simple enough

    @staticmethod
    def generate_groundfactrenamed_bodies(body, groundfact):
        indices = [i for i in range(len(body)) if (body[i].functor,body[i].arity) == (groundfact.functor, groundfact.arity)]
        for i in range(1, 1 << len(indices)):
            body_frags = [b for b in body]
            for j in range(len(indices)):
                mask = 1 << j
                if i & mask:
                    body_frags[indices[j]] =  ThetaSubsumptionLHM.new_groundfact_rename( body_frags[indices[j]] )
            yield body_frags

    def _propagate_to_rule_and_grind(self, rule, groundfact, new_groundings):
        # Optimization - We can force the new groundfact to be used by renaming it to something unique,
        # and replacing atleast one of the occurences in the rule body to the unique name   
        
        renamed_groundfact =  self.new_groundfact_rename(groundfact)
        if len(self._HAX_SS) > 0:
            db_string = "[%s, %s]"%(",".join(map(str,self._HAX_SS)), renamed_groundfact)
        else:
            db_string = "[%s]"%(renamed_groundfact)
        
        subbed_heads = set() 
        subtle_string_template = "subsumes_pyswip(%s, %s)"%("%s", db_string)
        for renamed_body_terms in self.generate_groundfactrenamed_bodies(rule.get_body(), groundfact):
            query_string = "[%s]"%(",".join(map(str,renamed_body_terms)))
            subtle_string = subtle_string_template%(query_string)
            
            subs = list(self._HAX_SUBTLE.query(subtle_string))
            subbed_heads.update(rule.ground_head(s) for s in subs)
        
        # print(subtle_string)
        # print(subbed_heads)
        new_groundings.update(subbed_heads)



    # def _inefficient_propagate_to_rule_and_grind(self, rule, groundfact, new_groundings):
    #     # Optimization - We can force the new groundfact to be used by renaming it to something unique,
    #     # and replacing atleast one of the occurences in the rule body to the unique name   
    #     renamed_groundfact =  str(groundfact)
    #     if len(self._HAX_SS) > 0:
    #         db_string = "[%s, %s]"%(",".join(map(str,self._HAX_SS)), renamed_groundfact)
    #     else:
    #         db_string = "[%s]"%(renamed_groundfact)
        
    #     subbed_heads = set() 
    #     query_string = str(rule.body)
    #     subtle_string = "subsumes_pyswip(%s, %s)"%(query_string, db_string)

    #     # print(subtle_string)
    #     subs = list(self._HAX_SUBTLE.query(subtle_string))
    #     # print("subs= ", subs)
    #     subbed_heads.update(rule.ground_head(s) for s in subs)
        
    #     new_groundings.update(subbed_heads)

    
