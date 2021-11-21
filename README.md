nilookup
--

**nilookup** is a small tool to search for the label of a brain area given its coordinate in MNI space. 
 **nilookup** is based on **nilearn**.

Requirements
--
- [nilearn](https://nilearn.github.io/stable/index.html) 0.8.1

Setup
--
Just download the [nilookup.py file](nilookup.py) and run the commands below from the same folder. 

Features
--

Currently **nilookup** uses a very basic principle ; it uses the following three brain atlases:
- Harvard Oxford cortical atlas, max probability with no threshold, 2mm resolution ('cort-maxprob-thr0-2mm')
- Destrieux atlas 2009
- Juelich atlas, max probability with no threshold, 2mm resolution ('maxprob-thr0-2mm')

Each of this atlas is a 3D atlas, as it is either a labels atlas or a max probability. So each (X,Y,Z) coordinate corresponds to a single label. 

**nilookup** generates a csv with the associated labels for each provided MNI coordinate. 

Usage
--

A search of a single coordinate can be done like this : 

    python nilookup.py -x 2 -y -18 -z 72

This should return 

       x_MNI  y_MNI  z_MNI    Harvard Oxford                 Destrieux                 Juelich    name
    0      2    -18     72  Precentral Gyrus  b'R G_and_S_paracentral'  GM Premotor cortex BA6  noname

It is also possible to provide a csv file as input. The csv file must be formatted as follows

    x,y,z,name
    2,-18,72,'Example'
    -50,-16,10,'Example 2'
    50,-16,10,'Example 3'

You can therefore provide it to **nilookup** like this : 

    python nilookup.py -i test.csv

and this will return 

        x_MNI  y_MNI  z_MNI                       Harvard Oxford                   Destrieux                           Juelich          name
    0      2    -18     72                     Precentral Gyrus    b'R G_and_S_paracentral'            GM Premotor cortex BA6     'Example'
    1    -50    -16     10  Heschl's Gyrus (includes H1 and H2)  b'L G_temp_sup-G_T_transv'  GM Primary auditory cortex TE1.0   'Example 2'
    2     50    -16     10  Heschl's Gyrus (includes H1 and H2)  b'R G_temp_sup-G_T_transv'  GM Primary auditory cortex TE1.0  'Example 3 '

The full list of arguments can be obtained like this : 

    python nilookup.py --h

    usage: nilookup.py [-h] [-x X] [-y Y] [-z Z] [-i I] [-o O]

    optional arguments:
    -h, --help  show this help message and exit
    -x X        X coordinate in MNI
    -y Y        Y coordinate in MNI
    -z Z        Z coordinate in MNI
    -i I        Path to a csv file in which each row is x,y,z,name
    -o O        Write the output to a csv file


Credits
--
Nicolas Farrugia, Tudor Popescu