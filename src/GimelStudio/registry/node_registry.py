## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## FILE: node_registry.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define the Node Registry
## ----------------------------------------------------------------------------

from GimelStudio.utils import exceptions


REGISTERED_NODES = {}

 
def RegisterNode(node, idname=""):
    """ Attempts to register a new node with the Node Registry.

    :param nodedef: subclass of NodeBase defining the node to be registered
    :param idname: type identifier of the node to be registered
    """
    if idname == "":
        raise TypeError("This node does not have an id name specified!")
    else:
        if idname in REGISTERED_NODES:
            raise exceptions.NodeExistsError(idname)

        REGISTERED_NODES[idname] = node


def CreateNode(parent, node_type, position, wx_id):
    """ Create an instance of a node associated with the specified name. 

    :param parent: parent of the node object (usually a wx.Window)
    :param node_type: type of node from registry - the IDName
    :param position: default position for the node
    :param wx_id: id for the node. Usually an id generated by wxPython.

    :returns: Node object
    :raises: NodeNotFoundError if the node is not registered in the Node Registry
    """
    if node_type in REGISTERED_NODES:
        # Initialize the base class here so that a new instance 
        # is created for each node. We also set some important
        # values for the position and type of the node.
        node = REGISTERED_NODES[node_type]
        node  = node(wx_id)
        node.SetPosition(position)
        node.Model.SetType(node_type)
        node.Model.SetParent(parent)
        return node
    else:
        raise exceptions.NodeNotFoundError(node_type)