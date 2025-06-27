#!/bin/bash

# Deploy EcuapassBot to github wintest or win repo"
# Copy EcuapassBot links to newdir and link .git to new dir

echo "Deploy EcuapassBot to github wintest or win repo"
echo ""

# Check if no params
if [ -z "$1" ]; then
    echo "USAGE: ebotdeploy.sh <wintest|win>"
    exit 1
fi

# define dirs
GITREPO="$1"                  # Suffix: "wintest" or "win"
GITREPODIR=EcuapassBot7-$GITREPO
LINKSDIR=EcuapassBot7-links   # Links
GITDIR=GIT  # Deploy dir

# Copy links to files
rsync -Lra $LINKSDIR $GITDIR
mv $GITDIR/$LINKSDIR/ $GITDIR/$GITREPODIR
#rmdir $GITDIR/$LINKSDIR

# Add .git
ln -s ../../$GITREPODIR/.git $GITDIR/$GITREPODIR

