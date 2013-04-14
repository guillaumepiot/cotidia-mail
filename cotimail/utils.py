import cssutils, re


# This function will read the CSS at the top of the page, 
# then apply it inline accordingly to each HTML tag

def inline_css(message):
    
    # Get our css
    zone =  u'<style.*>(.*)</style>'
    css = re.findall(zone, message, re.DOTALL)
    
    if len(css) > 0:
        sheet = cssutils.parseString(css[0])     

        email_font = False
        for rule in sheet:
        
            #print rule  
            if hasattr(rule, 'selectorText'):
                if rule.selectorText == 'body':
                    for s in rule.style:
                        if s.name == 'font-family':
                            # Apply the font-family throughout
                            email_font = str(s.value)
                    
                
                completestyle = ""
                if email_font:
                    completestyle = completestyle+"font-family:"+email_font+";"
            
                if hasattr(rule, 'style'):
                    for s in rule.style:
                        completestyle = completestyle + str(s.name) +":"+ str(s.value) +";"
                        completestyle = completestyle.replace('"',"'")
            
                # Class CSS replacement
                _class = rule.selectorText.split('.')
                if len(_class) == 2:
                    element = re.compile(r'class="'+str(_class[1])+'"', re.DOTALL)
                    replacement = " style=\""+completestyle+"\" "
                    message = element.sub(replacement,message)

                # ID CSS replacement
                _id = rule.selectorText.split('#')
                if len(_id) == 2:
                    element = re.compile(r'id="'+str(_id[1])+'"', re.DOTALL)
                    replacement = " style=\""+completestyle+"\" "
                    message = element.sub(replacement,message)
            
                if rule.selectorText == 'a':
                    element = re.compile(u'<'+str(rule.selectorText), re.DOTALL)
                    replacement = '<'+str(rule.selectorText)+" style=\""+completestyle+"\" "
                else:
                    element = re.compile(u'<'+str(rule.selectorText)+'>', re.DOTALL)
                    replacement = '<'+str(rule.selectorText)+" style=\""+completestyle+"\" >"
            
                message = element.sub(replacement,message)

        # Remove style from the head
        #regex = re.compile(r"<style.*>.*</style>",  re.DOTALL)
        #message = regex.sub(r"", message)

    else:
        # No style sheet available in this template
        pass


    
    return message