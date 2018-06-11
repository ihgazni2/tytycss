import re
import copy
import html
import tinycss2 as tycss
import elist.elist as elel
import estring.estring as eses
import tlist.tlist as tltl
import edict.edict as eded
from xdict.jprint import print_j_str
from xdict.jprint import pobj
from xdict.jprint import convert_token_in_quote 


#prld  prelude
#cntnt content
#one   preludeElement-or-contentElement
#dcd   decode
#dcds1 decode-stage-1
#rmwsp remove-white-spaces-element
#
def read_file(fn):
    fd = open(fn,'r+')
    rslt = fd.read()
    fd.close()
    return(rslt)

def write_file(fn,s):
    fd = open(fn,'w+')
    fd.write(s)
    fd.close()


def has_property(obj,name):
    attribs = dir(obj)
    cond1 = name in attribs
    return(cond1)

def gen_dummy_atrule():
    input = '''@dummy (dummy:dummy) {dummy{}}'''
    cssbyts = input.encode('utf-8')
    rules,codec = tycss.parse_stylesheet_bytes(cssbyts)
    return(rules[0])



def dcds1_norecur(one):
    '''
        norecur
    '''
    d = {
        "type":None,
        "value":None,
        "unit":None,
        "content":None,
        "name":None,
        "arguments":None
    }
    condt = has_property(one,'type')
    condv = has_property(one,'value')
    condu = has_property(one,'unit')
    condc = has_property(one,'content')
    condn = has_property(one,'name')
    conda = has_property(one,'arguments')
    if(condt):
        d['type'] = one.type
    else:
        pass
    if(condv):
        d['value'] = one.value
    else:
        pass
    if(condu):
        d['unit'] = one.unit
    else:
        pass
    if(condc):
        d['content'] = one.content
    else:
        pass
    if(condn):
        d['name'] = one.name
    else:
        pass
    if(conda):
        d['arguments'] = one.arguments
    else:
        pass
    return(d)

def dcds1_is_leaf(d):
    condc = (d['content'] == None)
    conda = (d['arguments'] == None)
    return(condc&conda)

def dcds1_get_children(d,ppl):
    curr = eded._getitem_via_pathlist(d,ppl)
    plsuffix = None
    if(curr['content'] != None):
        rchildren = elel.array_map(curr['content'],dcds1_norecur)
        value_map_func_args = [ppl,'content']
        plsuffix = 'content'
    elif(curr['arguments'] != None):
        rchildren = elel.array_map(curr['arguments'],dcds1_norecur)
        value_map_func_args = [ppl,'arguments']
        plsuffix = 'arguments'
    else:
        rchildren = []
        value_map_func_args = [ppl]
    def index_map_func(index):
        return(index)
    def value_map_func(index,ele,ppl,plsuffix):
        pl = copy.deepcopy(ppl)
        pl.append(plsuffix)
        pl.append(index)
        return({"data":ele,"pl":pl})
    children = elel.array_dualmap(rchildren,index_map_func=index_map_func,value_map_func=value_map_func,value_map_func_args=value_map_func_args)
    return((children,rchildren,plsuffix))

# rule content arguments
def dcds1(one):
    '''
        recur
    '''
    d = dcds1_norecur(one)
    ele = {'data':d,'pl':[]}
    unhandled = [ele]
    while(unhandled.__len__()>0):
        #yield(d)
        next_unhandled = []
        for i in range(0,unhandled.__len__()):
            ele = unhandled[i]
            data = ele['data']
            ppl = ele['pl']
            cond = dcds1_is_leaf(data)
            if(cond):
                pass
            else:
                children,rchildren,plsuffix = dcds1_get_children(d,ppl)
                cpl = copy.deepcopy(ppl)
                if(plsuffix == None):
                    pass
                else:
                    cpl.append(plsuffix)
                eded._setitem_via_pathlist(d,cpl,rchildren)
                next_unhandled = elel.concat(next_unhandled,children)
        unhandled = next_unhandled
    return(d)

#
def dcds1_prelude(prelude):
    dummy = gen_dummy_atrule()
    dummy.content = prelude
    #dummy.type = 'prelude'
    return(dcds1(dummy))

##########################

####################
#cntnt dict 

def cntnt_fmt_norecur(content):
    if(content.__len__() == 0):
        return([])
    else:
        if(content[0]['type']=='whitespace'):
            content = content[1:]
        else:
            pass
        if(content[-1]['type']=='whitespace'):
            content = content[:-1]
        else:
            pass
    return(content)

def cntnt_is_leaf(ele):
    '''
    '''
    cond = (ele['content'] == None)
    return(cond)

def cntnt_get_children(ele,ppl):
    '''
    '''
    #t = ele['type']
    content = ele['content']
    content = cntnt_fmt_norecur(content)
    value_map_func_args = [ppl]
    def index_map_func(index):
        return(index)
    def value_map_func(index,ele,ppl):
        pl = copy.deepcopy(ppl)
        pl.append('content')
        pl.append(index)
        return({"data":ele,"pl":pl})
    children = elel.array_dualmap(content,index_map_func=index_map_func,value_map_func=value_map_func,value_map_func_args=value_map_func_args)
    return(children)

def cntnt_init_unhandled(content):
    '''
        content is a list
    '''
    def index_map_func(index):
        return(index)
    def value_map_func(index,ele):
        return({"data":ele,"pl":[index]})
    unhandled = elel.array_dualmap(content,index_map_func=index_map_func,value_map_func=value_map_func)
    return(unhandled)

####################

#rslt 
def cntnt_rm_whitespace(content):
    content = cntnt_fmt_norecur(content)
    rslt = elel.init(content.__len__())
    unhandled = cntnt_init_unhandled(content)
    while(unhandled.__len__()>0):
        next_unhandled = []
        for i in range(0,unhandled.__len__()):
            ele = unhandled[i]
            data = ele['data']
            ppl = ele['pl']
            cond = cntnt_is_leaf(data)
            if(cond):
                rslt = elel.setitem_via_pathlist(rslt,data,ppl)
            else:
                children = cntnt_get_children(data,ppl)
                rchildren = elel.array_map(children,lambda child:child['data'])
                dummy = copy.deepcopy(data)
                dummy['content'] = rchildren
                rslt = elel.setitem_via_pathlist(rslt,dummy,ppl)
                next_unhandled = elel.concat(next_unhandled,children)
        unhandled = next_unhandled
    return(rslt)


##################



####################
#encd encode 
def encd_dimension(d):
    '''
        d = {
             'content': None,
             'name': None,
             'type': 'dimension',
             'arguments': None,
             'unit': 'px',
             'value': 900.0
        }
        encd_dimension(d)
    '''
    return(str(d['value'])+str(d['unit']))

def encd_percentage(d):
    '''
        d = {
                'content': None,
                'name': None,
                'value': -50.0,
                'arguments': None,
                'unit': None,
                'type': 'percentage'
        }
        encd_percentage(d)
    '''
    return(str(d['value'])+"%")

def encd_arguments(args):
    '''
        args = [
                   {
                    'content': None,
                    'name': None,
                    'value': -50.0,
                    'arguments': None,
                    'unit': None,
                    'type': 'percentage'
                   },
                   {
                    'content': None,
                    'name': None,
                    'value': ',',
                    'arguments': None,
                    'unit': None,
                    'type': 'literal'
                   },
                   {
                    'content': None,
                    'name': None,
                    'value': -50.0,
                    'arguments': None,
                    'unit': None,
                    'type': 'percentage'
                   },
              ],
        encd_arguments(args)
    '''
    args = elel.filter(args,lambda ele:(ele['type']!='whitespace'))
    args = elel.array_map(args,encd_one)
    s = '(' + elel.join(args,'') +')'
    return(s)

def encd_function(d):
    '''
        d = {
         'content': None,
         'name': 'translateY',
         'value': None,
         'arguments':
                      [
                       {
                        'content': None,
                        'name': None,
                        'value': -50.0,
                        'arguments': None,
                        'unit': None,
                        'type': 'percentage'
                       }
                      ],
         'unit': None,
         'type': 'function'
        }
        encd_dimension(d)
    '''
    s = str(d['name']) + encd_arguments(d['arguments'])
    return(s)

def encd_cntnt_atkey(d):
    '''
        d = {
         'content': None,
         'name': None,
         'type': 'at-keyword',
         'arguments': None,
         'unit': None,
         'value': 'media'
        }
        encd_cntnt_atkey(d)
    '''
    return("@" + str(d['value']))


def encd_other(d):
    return(str(d['value']))



def encd_hash(d):
    return("#" + str(d['value']))


def encd_one(d):
    if(d['type'] == 'dimension'):
        s = encd_dimension(d)
    elif(d['type'] == 'percentage'):
        s = encd_percentage(d)
    elif(d['type'] == 'function'):
        s = encd_function(d)
    elif(d['type'] == 'hash'):
        s = encd_hash(d)
    elif(d['type'] == 'at-keyword'):
        s = encd_cntnt_atkey(d)
    else:
        s = encd_other(d)
    return(s)






def encd_square_blk(d,for_display=False):
    '''
        #for beautifier
        #[ \x01
        #] \x02
        d =  {
                'content':
                           [
                            {
                             'content': None,
                             'name': None,
                             'type': 'ident',
                             'arguments': None,
                             'unit': None,
                             'value': 'title'
                            },
                            {
                             'content': None,
                             'name': None,
                             'type': 'literal',
                             'arguments': None,
                             'unit': None,
                             'value': '~='
                            },
                            {
                             'content': None,
                             'name': None,
                             'type': 'ident',
                             'arguments': None,
                             'unit': None,
                             'value': 'hello'
                            }
                           ],
                'name': None,
                'type': '[] block',
                'arguments': None,
                'unit': None,
                'value': None
        }
        encd_square_blk(d)
    '''
    c = cntnt_fmt_norecur(d['content'])
    arr = elel.array_map(c,encd_one)
    s = elel.join(arr,"")
    if(for_display):
        s ='\x01'+s+'\x02'
    else:
        s ='['+s+']'
    return(s)

def encd_paren_blk(d):
    '''
        d = {
            'content':
                         [
                          {
                           'content': None,
                           'name': None,
                           'value': 'min-width',
                           'arguments': None,
                           'unit': None,
                           'type': 'ident'
                          },
                          {
                           'content': None,
                           'name': None,
                           'value': ':',
                           'arguments': None,
                           'unit': None,
                           'type': 'literal'
                          },
                          {
                           'content': None,
                           'name': None,
                           'value': 900.0,
                           'arguments': None,
                           'unit': 'px',
                           'type': 'dimension'
                          }
                         ],
              'name': None,
              'value': None,
              'arguments': None,
              'unit': None,
              'type': '() block'
        }
    '''
    c = cntnt_fmt_norecur(d['content'])
    paren = elel.array_map(c,encd_one)
    s = elel.join(paren,"")
    s ='('+s+')'    
    #d = scil2dict(paren)
    #t = (d,)
    return(s)

def cntnt2cil(content,for_display=False):
    ####for comments
    if(content == None):
        return([])
    else:
        pass
    ####
    content = cntnt_fmt_norecur(content)
    rslt = elel.init(content.__len__())
    unhandled = cntnt_init_unhandled(content)
    while(unhandled.__len__()>0):
        next_unhandled = []
        for i in range(0,unhandled.__len__()):
            ele = unhandled[i]
            data = ele['data']
            ppl = ele['pl']
            cond = cntnt_is_leaf(data)
            rpl = elel.remove_all(ppl,'content')
            if(cond):
                s = encd_one(data)
                rslt = elel.setitem_via_pathlist(rslt,s,rpl)
            else:
                # treat square_blk as a leaf
                if(data['type'] == '[] block'):
                    s = encd_square_blk(data,for_display)
                    rslt = elel.setitem_via_pathlist(rslt,s,rpl)
                # treat paren_blk as a leaf
                elif(data['type'] == '() block'):
                    s = encd_paren_blk(data)
                    rslt = elel.setitem_via_pathlist(rslt,s,rpl)
                else:
                    children = cntnt_get_children(data,ppl)
                    dummy = elel.init(children.__len__())
                    rslt = elel.setitem_via_pathlist(rslt,dummy,rpl)
                    next_unhandled = elel.concat(next_unhandled,children)
        unhandled = next_unhandled
    return(rslt)


#####################

def get_atkey(rule):
    if(has_property(rule,'at_keyword')):
        return("@" + rule.at_keyword)
    else:
        return("")

def get_prelude_cil(rule,for_display=False):
    if(has_property(rule,'prelude')):
        p = dcds1_prelude(rule.prelude)
        cil = cntnt2cil(p['content'],for_display)
    else:
        cil =[]
    return(cil)

SELLITS = ['.','*','#',',','>','+',':','~']
SELATTANEXTS = ['.','#']
SELATTABOTHS = [',','>','+',':','~']
#
def prelude_cil2str(cil):
    '''
    '''
    if(cil.__len__()==0):
        return("")
    else:
        pass
    ####
    def cond_func(s):
        s = eses.replace(s,re.compile("[\x20]+"),"\x20")
        return(s)
    ####
    cil = elel.array_map(cil,cond_func)
    ####
    lngth = cil.__len__()
    ####
    prev = cil[0]
    ncil = [prev]
    ####
    i = 1
    while(i<(lngth-1)):
        prev = cil[i-1]
        curr = cil[i]
        nxt = cil[i+1]
        ########PREV########
        if(curr in SELATTABOTHS):
            if(prev == "\x20"):
                ncil.pop(-1)
            else:
                pass
        else:
            pass
        ########NEXT########
        if(curr in SELATTANEXTS):
            if(nxt == "\x20"):
                #no need whitespace after "."
                i = i + 1
                ncil.append(curr)
            else:
                ncil.append(curr)
        elif(curr in SELATTABOTHS):
            if(nxt == "\x20"):
                #no need whitespace after 
                i = i + 1
                ncil.append(curr)
            else:
                ncil.append(curr)
        else:
            ncil.append(curr)
        i = i +1
    ####
    if(lngth > 1):
        prev = cil[lngth-2]
        curr = cil[lngth-1]
        if(curr in SELATTABOTHS):
            if(prev == "\x20"):
                ncil.pop(-1)
            else:
                pass
        else:
            pass
        ncil.append(curr)
        #########
        if(ncil[0] in SELATTANEXTS):
            if(ncil[1] == "\x20"):
                ncil.pop(1)
            else:
                pass
        else:
            pass
    else:
        pass
    ####
    ####
    s = elel.join(ncil,"")
    s =eses.replace(s,re.compile("[\x20]+"),"\x20")
    return(s.strip('\x20'))


def get_prelude_str(rule):
    cil = get_prelude_cil(rule)
    s = prelude_cil2str(cil)
    return(s)

def get_content_cil(rule,for_display=False):
    c = dcds1(rule)
    cil = cntnt2cil(c['content'],for_display)
    return(cil)

###########################################


def get_css_rule_cil(rule):
    ats = get_atkey(rule)
    head = [ats]
    pcil = get_prelude_cil(rule)
    head = elel.concat(head,pcil)
    c = dcds1(rule)
    ccil = cntnt2cil(c['content'],for_display=False)
    rslt = [head,ccil]
    return(rslt)



def get_css_rule_str(d):
    lines = print_j_str(d.__str__(),with_color=False,fixed_indent=True)
    s = elel.join(lines,'\n')
    s = s.replace('[\n','{\n')
    s = s.replace(']\n','}\n')
    s = s.replace(':\x20\n','\n')
    s = s.replace(',\x20\n','\n')
    s = convert_token_in_quote(s)
    s = s .replace("'","")
    s = html.unescape(s)
    s = s.strip('\x20').strip('\n').strip('\x20')
    if(s[-1] == "]"):
        s = s[:-1] + '}'
    else:
        pass
    return(s)



#########search###############
def get_dummy_sel_rule(sel):
    '''
    '''
    input = sel + '{}'
    cssbyts = input.encode('utf-8')
    rules,codec = tycss.parse_stylesheet_bytes(cssbyts)
    return(rules[0])


def sel_fmt(sel):
    '''
       sel selector-string
    '''
    r = get_dummy_sel_rule(sel)
    p = get_prelude_cil(r)
    return(p)


def slct_cond_func(rule,sel,mode="loose"):
    p = get_prelude_cil(rule)
    if(mode=="loose"):
        cond = elel.comprise(p,sel,mode="loose")
    else:
        cond = (p == sel)
    return(cond)

def slct_all(rules,sel,mode="loose"):
    sel = sel_fmt(sel)
    rules = elel.filter(rules,slct_cond_func,sel,mode)
    return(rules)

def slct_which(rules,sel,which,mode="loose"):
    sel = sel_fmt(sel)
    tmp = elel.find_which(rules,which,slct_cond_func,sel,mode)
    r = tmp['value']
    if(r==None):
        return("")
    else:
        return(r)

def slct_first(rules,sel,mode="loose"):
    return(slct_which(rules,sel,0,mode))

def slct_last(rules,sel,mode="loose"):
    return(slct_which(rules,sel,-1,mode))

##
def slct_at_cond_func(rule,atsel,mode="loose"):
    at = get_atkey(rule)
    if(mode=="loose"):
        cond = (atsel in at)
    else:
        cond = (at == atsel)
    return(cond)

def slct_at_all(rules,atsel,mode="loose"):
    rules = elel.filter(rules,slct_at_cond_func,atsel,mode)
    return(rules)

def slct_at_which(rules,atsel,which,mode="loose"):
    tmp = elel.find_which(rules,which,slct_at_cond_func,atsel,mode)
    r = tmp['value']
    if(r==None):
        return("")
    else:
        return(r)

def slct_at_first(rules,atsel,mode="loose"):
    return(slct_at_which(rules,atsel,0,mode))

def slct_at_last(rules,atsel,mode="loose"):
    return(slct_at_which(rules,atsel,-1,mode))

##
def get_rules_from_str(input,codec='utf-8'):
    cssbyts = input.encode(codec)
    rules,codec = tycss.parse_stylesheet_bytes(cssbyts)
    rules = elel.filter(rules,lambda rule:(rule.type!='whitespace'))
    return(rules)

def get_rules_from_file(fn,codec='utf-8'):
    input = read_file(fn)
    return(get_rules_from_str(input,codec))

def get_rules(codec='utf-8',**kwargs):
    if('fn' in kwargs):
        fn = kwargs['fn']
        return(get_rules_from_file(fn,codec))
    else:
        input = kwargs['input']
        return(get_rules_from_str(input,codec))



def serialize_array(arr):
    arr = elel.array_map(arr,lambda ele:ele.serialize())
    s = elel.join(arr,"")
    s = s.replace('\t',"")
    s = s.replace('\r',"")
    s = s.replace('\n',"")
    s = s.strip('\x20')
    s = eses.replace(s,re.compile("[\x20]+"),"\x20")
    return(s)

#4e four-elements-dict
def new_four_elements():
    d = {
        'at':None,
        "prelude":None,
        "content":None,
        "type":None
    }
    return(d)

def gen_4e(rule,prelude='list'):
    d = new_four_elements()
    d['type'] = rule.type
    d['at'] = get_atkey(rule)
    d['prelude'] = get_prelude_cil(rule)
    if(prelude == "list"):
        pass
    else:
        d['prelude'] = prelude_cil2str(d['prelude'])
    if(has_property(rule,'content')):
        if(rule.content==None):
            d['content'] = ""
        else:
            d['content'] = serialize_array(rule.content)
    else:
        tmp = dcds1_norecur(rule)
        d['content'] = encd_one(tmp)
    return(d)

def srlz2rule(s,codec="utf-8"):
    rules= get_rules_from_str(s,codec)
    return(rules[0])

def srlz2rules(s,codec="utf-8"):
    rules= get_rules_from_str(s,codec)
    return(rules)

def srlz_rule_is_leaf(rule,codec="utf-8"):
    if(rule.type == 'error'):
        return(True)
    else:
        return(False)

def srlz_value_map_func(index,child,ppl,prelude):
    d = gen_4e(child,prelude)
    pl = copy.deepcopy(ppl)
    pl.append(index)
    return({"data":d,"pl":pl})

def srlz_index_map_func(index,si):
    return(index+si)

def srlz_get_children_from_rules(rules,si,ppl,prelude,codec="utf-8"):
    children = rules
    children = elel.array_dualmap(
                   children,
                   index_map_func = srlz_index_map_func,
                   index_map_func_args = [si],
                   value_map_func = srlz_value_map_func,
                   value_map_func_args = [ppl,prelude]
               )
    return(children)

def srlz_get_children(data,si,ppl,prelude,codec="utf-8"):
    s = data['content']
    rules = srlz2rules(s,codec)
    children = srlz_get_children_from_rules(rules,si,ppl,prelude,codec)
    return(children)

def fe_is_leaf(obj,codec="utf-8"):
    if(isinstance(obj,list)):
        rules = obj
    elif(isinstance(obj,string)):
        rules = srlz2rules(obj,codec="utf-8")
    else:
        s = obj['content']
        rules = srlz2rules(s,codec="utf-8")
    if(rules.__len__()>1):
        return(False)
    else:
        rule = rules[0]
        if(rule.type == "error"):
            return(True)
        else:
            return(False)

#desc mat 
#prelude='list',codec='utf-8'
#content = 'dict' 
#cbs 'float:none;display:block;'


def cbs_fmt(cbs,**kwargs):
    '''
       cbs = 'float:none;display:block;'
       cbs = 'float:none;display:block'
       cbs = 'font-family: "Droid Sans", arial, sans-serif; font-weight: bold; font-size: 14px;'
       
    '''
    if('sp' in kwargs):
        sp = kwargs['sp']
    else:
        sp = ';'
    cbs = convert_token_in_quote(cbs,colons=[";"])
    cbs = cbs.replace("&#59;","")
    cbs = html.unescape(cbs)
    cbs = cbs.strip(sp)
    arr = cbs.split(sp)
    arr = elel.array_map(arr,lambda ele:(ele+sp))
    return(arr)



def gen_4e_mat(rule,**kwargs):
    if("codec" in kwargs):
        codec = kwargs['codec']
    else:
        codec = 'utf-8'
    if("prelude" in kwargs):
        prelude = kwargs['prelude']
    else:
        prelude ='str'
    if("content" in kwargs):
        content = kwargs['content']
    else:
        content ='format'
    mat = []
    d = gen_4e(rule,prelude)
    root = {
        "data":d,
        "pl":[0]
    }
    unhandled = [root]
    while(unhandled.__len__()>0):
        next_unhandled = []
        mat.append([])
        level = mat[mat.__len__() -1]
        for i in range(0,unhandled.__len__()):
            ele = unhandled[i]
            data = ele['data']
            ppl = ele['pl']
            #####
            rules = srlz2rules(data['content'])
            ####
            cond = fe_is_leaf(rules)
            if(cond):
                ele['leaf'] = True
                if(content == 'format'):
                    data['content'] = cbs_fmt(data['content'])
                else:
                    pass
            else:
                ele['leaf'] = False
                si = next_unhandled.__len__()
                children = srlz_get_children_from_rules(rules,si,ppl,prelude,codec)
                next_unhandled = elel.concat(next_unhandled,children)
            level.append(ele)
        unhandled = next_unhandled
    return(mat)

def gen_show_mat(mat,rtrn=False):
    for i in range(0,mat.__len__()):
        level = mat[i]
        for j in range(0,level.__len__()):
            if(rtrn):
                yield({(i,j):level[j]})
            else:
                print("[{0}][{1}]".format(i,j))
                pobj(level[j]['data'])
                yield((i,j))

class ShowMat():
    def __init__(self,mat,**kwargs):
        if(isinstance(mat,list)):
            pass
        else:
            mat = gen_4e_mat(mat)
        if('rtrn' in kwargs):
            self.rtrn = kwargs['rtrn']
        else:
            self.rtrn = False
        self.gen = gen_show_mat(mat,self.rtrn)
    def next(self):
        if(self.rtrn):
            return(self.gen.__next__())
        else:
            self.gen.__next__()


#############################
def recover_comment(content):
    comment = elel.join(content,'\n')
    comment ="\*" + comment + "*\\"
    return(comment)

############################


def matele2dict(ele):
    d = {}
    ele = ele['data']
    k = ""
    if(ele['type'] == 'at-rule'):
        k = k + ele['at']
    else:
        pass
    k = k + "\x20" + ele['prelude']
    k = k.strip('\x20')
    if(ele['type'] == 'comment'):
        v = recover_comment(ele['content'])
    else:
        v = ele['content']
    d[k] = v
    return(d)

#############################
def recover_comment(content):
    comment = elel.join(content,'\n')
    comment ="\*" + comment + "*\\"
    return(comment)

############################

def mat2dict(mat):
    mat = copy.deepcopy(mat)
    lngth = mat.__len__()
    for i in range(lngth-1,0,-1):
        level = mat[i]
        plseq = i-1
        for j in range(0,level.__len__()):
            ele = level[j]
            pseq = ele['pl'][-2]
            d = matele2dict(ele)
            if('doing' in mat[plseq][pseq]):
                mat[plseq][pseq]['data']['content'].append(d)
            else:
                mat[plseq][pseq]['doing'] = True
                mat[plseq][pseq]['data']['content'] = [d]
    d = matele2dict(mat[0][0])
    return(d)


class Rule():
    def __init__(self,rule,codec='utf-8'):
        if(isinstance(rule,str)):
            rules = get_rules_from_str(rule,codec)
            rule = rules[0]
        else:
            pass
        self.codec = codec
        self.atkey = get_atkey(rule)
        self.prelude_cil = get_prelude_cil(rule)
        self.prelude = prelude_cil2str(self.prelude_cil)
        self.content_cil = get_content_cil(rule)
        self.mat = gen_4e_mat(rule)
        self.dict = mat2dict(self.mat)
        self.head = list(self.dict.keys())[0]
        self.content = get_css_rule_str(self.dict[self.head])
        self.css_cil = get_css_rule_cil(rule)
        self.css = get_css_rule_str(self.dict)
        self.step = ShowMat(self.mat)
    def show(self):
        pobj(self.dict,fixed_indent=True)
    def mshow(self,depth=0,width=0):
        pobj(self.mat[depth][width]['data'])
    def more(self):
        try:
            self.step.next()
        except:
            self.step = ShowMat(self.mat)
            self.step.next()
        else:
            pass
    def lshow_prelude(self):
        pobj(self.prelude_cil)
    def lshow_content(self):
        pobj(self.content_cil)
    def lshow_css(self):
        pobj(self.css_cil)
    def show_prelude(self):
        print(self.prelude)
    def show_content(self):
        print(self.content)
    def show_css(self):
        print(self.css)

class CSS():
    def __init__(self,**kwargs):
        self.rules = get_rules(**kwargs)
        self.count = self.rules.__len__()
    def __getitem__(self,i):
        r = Rule(self.rules[i])
        return(r)
    def all(self,sel,mode="loose"):
        rs = slct_all(self.rules,sel,mode)
        rs = elel.array_map(rs,lambda r:Rule(r))
        return(rs)
    def which(self,sel,which,mode="loose"):
        r = slct_which(self.rules,sel,which,mode)
        r = Rule(r)
        return(r)
    def first(self,sel,mode="loose"):
        r = slct_first(self.rules,sel,mode)
        r = Rule(r)
        return(r)
    def last(self,sel,mode="loose"):
        r = slct_first(self.rules,sel,mode)
        r = Rule(r)
        return(r)
    def at_all(self,sel,mode="loose"):
        rs = slct_at_all(self.rules,sel,mode)
        rs = elel.array_map(rs,lambda r:Rule(r))
        return(rs)
    def at_which(self,sel,which,mode="loose"):
        r = slct_at_which(self.rules,sel,which,mode)
        r = Rule(r)
        return(r)
    def at_first(self,sel,mode="loose"):
        r = slct_at_first(self.rules,sel,mode)
        r = Rule(r)
        return(r)
    def at_last(self,sel,mode="loose"):
        r = slct_at_first(self.rules,sel,mode)
        r = Rule(r)
        return(r)
    def help(self):
        s = '''
            css = CSS(fn="2833_rules.css")
            rs = css.all("ul")
            rs[0].show_css()
            rs[0].mshow()
            rs[100].mshow()
            rs[100].prelude
            rs = css.at_all("media")
            rs.__len__()
            rs[0].show()
            rs[0].more()
            rs[0].more()
            rs[0].more()
            
        '''
        print(s)

#prelude 紧凑
#content 松散

def beautify_selpath(sel):
    cil = sel_fmt(sel)
    sel = prelude_cil2str(cil)
    return(sel)


def beautify_rule(input):
    css = CSS(input)
    arr = elel.array_map(css,trim_func)
    s = elel.join(arr,'\n')
    r = Rule(input)
    print(r.css)
    return(r.css)
   
def beautify_cssfile(src_file,dst_file):
    def trim_func(r):
        s = r.css
        s = s.strip('/n')
        s = eses.lstrip(s,'{',1)
        s = eses.rstrip(s,'}',1)
        return(s)
    css = CSS(fn=src_file)
    arr = elel.array_map(css,trim_func)
    s = elel.join(arr,'\n')
    write_file(dst_file,s) 
