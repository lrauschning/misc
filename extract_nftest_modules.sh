#!/bin/sh

# small script to extract the modules required by an nf-test test file
# and list them for automatic installation
# may required adjusting the call to nf-core modules install depending on local setup

module_name=$(basename $(echo modules/modules/nf-core/umitools/dedup/tests/main.nf.test | sed -e 's/[[:alnum:]]*\/tests\/[[:alnum:]]*.nf.test$//'))
# in real code:
#module_name=$(basename $(pwd | sed -e 's/[[:alnum:]]*\/tests\/[[:alnum:]].nf.test$//'))

# handle other tools
other_tools=$(grep -Poe 'script "\.\./\.\./\.\./.*"' $1 |
	sed -e 's/^script "..\/..\/..\///' |
	sed -e 's/\/main.nf"$//' |
	sort |
	uniq)

# handle different modules of the same tool
same_tool=$(grep -oe 'script "\.\./\.\./\w*/.*"' $1 |
	sed -e 's/^script "..\/..\///' |
	sed -e 's/\/main.nf"$//' |
	sort |
	uniq |
	sed "s/^/${module_name}\//" );

for module in $other_tools $same_tool; do
	echo nf-core modules install $module; # dry run
done
