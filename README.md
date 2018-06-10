# tytycss
>__search css file by selector-string/prelude-string__<br>
__a wrapped APIs for tinycss2__

# Install

>__pip3 install tytycss__

## Usage

>_click to see example_
-------------------------------------------------------
        
__1. ![load from input string](/Images/tyty.CSS.__init__0.png)__ 

    css = tyty.CSS(input=input) 
    

__2. load all css rules from a .css file__

    css = tyty.CSS(fn="tst1.css")  
![example]() 

__3. display__

    css.count
    r = css[2]
    r.atkey
    r.show_css()
    r.prelude
    r.head
    r.show_content()
![example]() 

__4. search in loose mode ,default is loose<br>    find all rules whose selectors-path includes 'ul'__   

    rs = css.all("ul")
![example]()

__5. __

![example]() 

-------------------------------------------------------

## Doc Help Man
-------------------------------------------------------
__6.__  

###### __6.1 __  

        
###### __6.2 __  

        
###### __6.3 __

        
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


## USEAGE SCREENSHOOTS

----------------------------------------------




![](/Images/.1.png)
![](/Images/.2.png)


        
![](/Images/.0.png)  



![](/Images/.0.png)



![](/Images/.0.png)



![](/Images/.0.png)

----------------------------------------------


## TODO
-----------------------------------------------

>__1. improve performance__ <br> 
__2. deep search__ <br>

-----------------------------------------------

