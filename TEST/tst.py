import tytycss.tytycss as tyty

# load from input string
    css = tyty.CSS(input=input)
# load all css rules from a .css file
    css = tyty.CSS(fn="tst1.css")
#display 
    css.count
    r = css[2]
    r.atkey
    r.show_css()
    r.prelude
    r.head
    r.show_content()



# search in loose mode ,default is loose
#find all rules whose selectors-path includes 'ul'
rs = css.all("ul")

# search in strict mode,
# find all rules whose selectors-path equals ".maincontent"
rs = css.all(".maincontent",mode="strict")

# search in loose mode
#find all rules whose selectors-path includes '.maincontent'
rs = css.all(".maincontent",mode="loose")

# single search 
r = css.first("ul")
r = css.last("ul")
r = css.which("ul",8)


#at_rule search
css = tyty.CSS(fn="2833_rules.css")
rs = css.at_all("media")
rs.count
r = css.at_first("media")
r = css.at_last("media")
r = css.at_which("media",5)



#advance show using
input = '''@media screen and (max-width: 300px) {
    body {
       background-color:lightblue;
    }
}'''

r = tyty.Rule(input)
#display as a dict
r.show()
#display at (depth,breadth), 
r.mshow(0,0)
# circlely show level by level
r.more()
r.more()
# list show
r.lshow_prelude()
r.lshow_content()
r.lshow_css()


# show internal dict
from xdict.jprint import pobj
pobj(r.dict)
pobj(r.dict,fixed_indent=True)
# show internal description mat
pobj(r.mat)





# beautify

tyty.beautify_selpath("a . test #oo")

input = '''span.more-link { float: left; display: block; }'''
formatted = tyty.beautify_rule(input)

tyty.beautify_cssfile("tst1.css","tst1.fmt.css")







#######################33

import tytycss.tytycss as tyty
# load from input string
# tyty.CSS.__init__0.png
input = '''
p 
{ 
 color:blue; 
 text-align:center; 
} 
.marked 
{ 
 background-color:red; 
} 
.marked p 
{ 
  color:white; 
}'''

css = tyty.CSS(input=input)
r = css[1]
r.show_css()



# load all css rules from a .css file
#  tyty.CSS.__init__1.png
css = tyty.CSS(fn="tst1.css")
css.count
r = css[2]
r.show_css()
r.prelude
r.show_content()

# at_rule 
#  tyty.CSS.__init__2.png
input = '''@media screen and (max-width: 300px) {
    body {
       background-color:lightblue;
    }
}'''
css = tyty.CSS(input=input)
r = css[0]
r.atkey
r.prelude
r.head
r.show_content()


# search loose mode ,default is loose
# tyty.CSS.all.loose.0.png
rs = css.all("ul")
rs.__len__()
rs[0].show_css()
rs[15].show_css()

# search in strict mode,
# find all rules whose selectors-path equals ".maincontent"
# tyty.CSS.all.strict.0.png
rs = css.all(".maincontent",mode="strict")
rs.__len__()
rs[0].prelude
rs[0].show_css()

# search in loose mode
#find all rules whose selectors-path includes '.maincontent'
#tyty.CSS.all.loose.1.png
rs = css.all(".maincontent",mode="loose")
rs.__len__()
rs[0].prelude
rs[0].show_css()
rs[1].prelude
rs[1].show_css()

#single search
#tyty.CSS.first_last_which.0.png
r = css.first("ul")
r.show_css()
r = css.last("ul")
r.show_css()
r = css.which("ul",8)
r.show_css()


#at_rule search
#tyty.CSS.at.0.png
css = tyty.CSS(fn="2833_rules.css")
rs = css.at_all("media")
rs.count
r = css.at_first("media")
r = css.at_last("media")
r = css.at_which("media",5)
r.show_css()
r.atkey
r.prelude













#advance show using
input = '''@media screen and (max-width: 300px) {
    body {
       background-color:lightblue;
    }
}'''

r = tyty.Rule(input)
#display as a dict
#tyty.CSS.show.0.png
r.show()

# tyty.CSS.mshow.0.png
#display at (depth,breadth), 
r.mshow(0,0)
# circlely show level by level
r.more()
r.more()

# list show
# tyty.CSS.lshow.0.png
r.lshow_prelude()
r.lshow_content()
r.lshow_css()


# show internal dict
# tyty.CSS.dshow.0.png
from xdict.jprint import pobj
pobj(r.dict)
pobj(r.dict,fixed_indent=True)

# tyty.CSS.matshow.1.png
# show internal description mat
pobj(r.mat)


# beautify
# tyty.CSS.beautify_rule.0.png
tyty.beautify_selpath("a . test #oo")

input = '''span.more-link { float: left; display: block; }'''
formatted = tyty.beautify_rule(input)

# tyty.CSS.beautify_file.0.png
tyty.beautify_cssfile("tst1.css","tst1.fmt.css")
# tyty.CSS.beautify_file.1.png
