# tytycss
>__search css file by selector-string/prelude-string__<br>
__a wrapped APIs for tinycss2__

# Install

>__pip3 install tytycss__

## Usage

>_click to see example_
-------------------------------------------------------
        
__1. ![load from input string](/Images/tyty.CSS.__init__0.png)__<br> 
     

        css = tyty.CSS(input=input) 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![at-rule input string](/Images/tyty.CSS.__init__2.png)  


__2. ![load all css rules from a .css file](/Images/tyty.CSS.__init__1.png)__

        css = tyty.CSS(fn="tst1.css")  
__3. ![display](/Images/tyty.Rule.display.0.png)__

        css.count
        r = css[2]
        r.atkey
        r.show_css()
        r.prelude
        r.head
        r.show_content()
__4. ![search in loose mode](/Images/tyty.CSS.all.loose.0.png)<br>    default is loose<br>    find all rules whose selectors-path includes 'ul'__   

        rs = css.all("ul")
__5. ![search in strict mode](/Images/tyty.CSS.all.strict.0.png)<br> find all rules whose selectors-path equals ".maincontent"__

        rs = css.all(".maincontent",mode="strict")

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![compare with loose mode](/Images/tyty.CSS.all.loose.1.png)  

__6. ![single search](/Images/tyty.CSS.first_last_which.0.png)__

        r = css.first("ul")
        r = css.last("ul")
        r = css.which("ul",8)
__7. ![at_rule search](/Images/tyty.CSS.at.0.png)__

        r = css.first("ul")
        r = css.last("ul")
        r = css.which("ul",8)

__8. ![beautify rule](/Images/tyty.CSS.beautify_rule.0.png)__

        tyty.beautify_selpath("a . test #oo")
        formatted = tyty.beautify_rule(input)

__10. beautify file__

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![before](/Images/tyty.CSS.beautify_cssfile.0.png)

        tyty.beautify_cssfile("tst1.css","tst1.fmt.css")
        
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![after](/Images/tyty.CSS.beautify_cssfile.1.png)


__11. ![show as dict](/Images/tyty.CSS.show.0.png)__
        
        r.show()
__12. ![level show](/Images/tyty.CSS.mshow.0.png)__

        #display at (depth,breadth), 
        r.mshow(0,0)
        # circlely show level by level
        r.more()
        r.more()

__13. ![list show](/Images/tyty.CSS.mshow.0.png)__

        r.lshow_prelude()
        r.lshow_content()
        r.lshow_css()
        
__14. ![internal_dict show](/Images/tyty.CSS.dshow.0.png)__
        
        from xdict.jprint import pobj
        pobj(r.dict)
        pobj(r.dict,fixed_indent=True)
 
 __15. ![internal_description mat show](/Images/tyty.CSS.matshow.0.png)__
 
        pobj(r.mat)

-------------------------------------------------------

## PACKAGE DEPENDANY

---------------------------------------------------------

[tinycss2](https://github.com/Kozea/tinycss2/blob/master/tinycss2)<br>
[xdict](https://github.com/ihgazni2/dlixhict-didactic)<br>
[elist](https://github.com/ihgazni2/elist)<br>
[edict](https://github.com/ihgazni2/edict)<br>
[tlist](https://github.com/ihgazni2/tlist)<br>
[estring](https://github.com/ihgazni2/estring)<br>

----------------------------------------------------------



----------------------------------------------


## TODO
-----------------------------------------------

>__1. improve performance__ <br> 
__2. deep search__ <br>

-----------------------------------------------

