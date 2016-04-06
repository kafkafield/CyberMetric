#include <Python.h> // this is in <python-install-path>/include folder  
#include <conio.h>  
#include <iostream>  
#include <string>  

using namespace std;

int main()
{
	string filename = "linkMySql"; // file name is settled!  
    string methodname = "getVulInfo"; // method name is also settled!  
    string expression = "CVE-2002-0392"; // get user input!  
    double result = 0.0;  
    // first init  
    Py_Initialize();  
    
	PyObject *pyFileName = PyString_FromString(filename.c_str());  
    PyObject *pyMod = PyImport_Import(pyFileName); // load the module 

    if(pyMod != NULL)
    {
    	PyObject *pyFunc = PyObject_GetAttrString(pyMod, methodname.c_str());  
    	if(pyFunc && PyCallable_Check(pyFunc))  
        {  
            PyObject *pyParams = PyTuple_New(1);  
            PyObject *pyValue = PyString_FromString(expression.c_str());  
            PyTuple_SetItem(pyParams, 0, pyValue);  
            // ok, call the function  
            pyValue = PyObject_CallObject(pyFunc, pyParams);  
            if(pyValue)  
            {  
                *result = PyFloat_AsDouble(pyValue);   
            } 
        }  
    }

    // last fini!  
    Py_Finalize();  

	return 0;
}