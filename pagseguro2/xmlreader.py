#==================================================
#xmlreader.py: Retrieved from http://code.activestate.com/recipes/116539/
# modified by leonardo.olsantos@gmail.com and francisco.v.vianna@gmail.com
#==================================================

class NotTextNodeError:
    pass


def getTextFromNode(node):
    """
    scans through all children of node and gathers the
    text. if node has non-text child-nodes, then
    NotTextNodeError is raised.
    """
    
    t = ""
    
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            t += n.nodeValue
        else:
            raise NotTextNodeError
    
    return t


def nodeToDic(node):
    """
    document2dict() scans through the children of node and makes a
    dictionary from the content.
    three cases are differentiated:
    - if the node contains no other nodes, it is a text-node
    and {nodeName:text} is merged into the dictionary.
    - else, nodeToDic() will call itself recursively on
    the nodes children (merging {nodeName:nodeToDic()} to
    the dictionary), making a list of nodes if multiple nodes with the same
    nodeName were found.
    """
    
    dic = {} 
    
    for n in node.childNodes:
        if n.nodeType != n.ELEMENT_NODE:
            continue
        try:
            text = getTextFromNode(n)
        except NotTextNodeError:
            # 'normal' node
            if n.nodeName in dic:
                elem = dic[str(n.nodeName)]
                if type(elem) == list:
                    elem.append(nodeToDic(n))
                else:
                    dic[str(n.nodeName)] = [elem, nodeToDic(n)]
            else:
                dic.update({str(n.nodeName):nodeToDic(n)})
            continue

        # text node
        dic.update({str(n.nodeName):text})
    
    return dic

document2dict = nodeToDic

def errors_to_list(errors_xml): # deprecated, use document2dict instead
    '''
        This piece of code is a little too specific and redundant.
        It will be incoporated to the rest of the code later. It's like this for now 
        so we can go on with more important things.
    '''
    error_list = []
    
    for error_node in errors_xml.firstChild.childNodes:
        dic = {}
        for c in error_node.childNodes:
            dic.update({c.nodeName:getTextFromNode(c)})
     
        error_list.append(dic)
            
    return error_list    
