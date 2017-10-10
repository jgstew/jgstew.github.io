In almost all cases, you should use Copy or Copy + Delete in BigFix ActionScript and not Move.

You might think that Copy + Delete is equivalent to Move in ActionScript, but at least in Windows, it is not.

I believe the difference is that a file copied will inherit permissions from the destination folder, while a file moved will not. I assume this means it inherits permissions from the origin folder, but I really don't know for sure.

I have run into issues where I use the move actionscript command to put a file on the system that all users should be able to read, including non-admins, but because I used the move command, they could not. Generally in my experience this is not the desired behavior unless the file being moved is a log file or something similar that you don't want most users to be able to read.


----------

### Related:

- https://forum.bigfix.com/t/always-use-copy-never-use-move-in-actionscript/23075
- https://developer.bigfix.com/action-script/reference/file/
- https://bigfix.me/cdb/fixlet/6250
