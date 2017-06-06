
# Git workflow illustrated

This post illustrates the common Git workflow. I created this especially for my own reference when working with git.


## Initial setup

* Coder1 has a repo that located at https://github.com/Coder1/git-test-1 is the master repo

* Coder1 did few commit on his repo

* Coder2 is interested on Coder1 work and want to do some collaboration 

* Coder2 forks Coder1's repo to https://github.com/Coder2/git-test-1 via github web UI

* After do the forking, Coder2 check his repo status 

    ```
    $ git log
    commit ffa646af70ecac7b84b9b0f80da3246d921280bd
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 10:41:41 2017 -0400

        create file.txt

    commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 10:39:45 2017 -0400

        first commit
    ```

* git log on Coder2's repo shows the complete history of all the changes made by Coder1
    


## Scenario 1: Sync between repo

* Coder1 makes a changes on his local repo, commit, and push it to github

    * check the status after change is made

        ```
        $ vim file.txt

        $ git status
        On branch master
        Your branch is up-to-date with 'origin/master'.
        Changes not staged for commit:
        (use "git add <file>..." to update what will be committed)
        (use "git checkout -- <file>..." to discard changes in working directory)

                modified:   file.txt

        no changes added to commit (use "git add" and/or "git commit -a")
        ```

    * compare the changes to the original file from the repo

        ```
        $ git diff file.txt
        diff --git a/file.txt b/file.txt
        index 8b0cc13..0b946aa 100644
        --- a/file.txt
        +++ b/file.txt
        @@ -1 +1,2 @@
        first
        +second
        ```

    * commit the changes to Coder1 local repo

        ```
        $ git commit -m "add second line" file.txt
        [master 70c7eba] add second line
        1 file changed, 1 insertion(+)
        ```

    * push the changes to github/remote repo

        ```
        $ git push
        Counting objects: 3, done.
        Compressing objects: 100% (2/2), done.
        Writing objects: 100% (3/3), 286 bytes | 0 bytes/s, done.
        Total 3 (delta 0), reused 0 (delta 0)
        To https://github.com/Coder1/git-test-1.git
        ffa646a..70c7eba  master -> master
        ```


    * verify the repo history

        ```
        $ git log
        commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:55:50 2017 -0400

            add second line

        commit ffa646af70ecac7b84b9b0f80da3246d921280bd
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:41:41 2017 -0400

            create file.txt

        commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:39:45 2017 -0400

            first commit
        ```


* Coder2 know that Coder1 did some changes, so coder to want to sync his local repo with Coder1 repo in github

    * Coder2 checks current history of his local repo which is the forked from Coder1 repo

        ```
        $ git log
        commit ffa646af70ecac7b84b9b0f80da3246d921280bd
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:41:41 2017 -0400

            create file.txt

        commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:39:45 2017 -0400

            first commit
        ```


    * Coder2 is trying to sync his repo to Coder1 github repo

        ```
        $ git fetch upstream
        fatal: 'upstream' does not appear to be a git repository
        fatal: Could not read from remote repository.

        Please make sure you have the correct access rights
        and the repository exists.
        ```

    * Coder2 sync attemp fails because Coder2 did not define Coder1 repo on his local git repo config 

    * Coder2 define Coder1 github repo as his "upstream"

        ```
        $ git remote add upstream https://github.com/Coder1/git-test-1.git
        ```
    
    * Coder2 is trying to sync again

        ```
        $ git fetch upstream
        remote: Counting objects: 3, done.
        remote: Compressing objects: 100% (2/2), done.
        remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
        Unpacking objects: 100% (3/3), done.
        From https://github.com/Coder1/git-test-1
        * [new branch]      master     -> upstream/master
        ```

    * Now the command works. Coder2's repo now should have Coder1's latest changes. Let's check now.

        ```
        (env) rwibawa1@ip-1-70-62-141:~/github/fork/git-test-1$ git log
        commit ffa646af70ecac7b84b9b0f80da3246d921280bd
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:41:41 2017 -0400

            create file.txt

        commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:39:45 2017 -0400

            first commit
        ```
	
	  * Hmm, it still has no Coder1's changes. This is correct because the upstream data has been pulled but has not been merged with the Coder2's local repo. Let's do it now.

	
        ```
        (env) rwibawa1@ip-1-70-62-141:~/github/fork/git-test-1$ git merge upstream/master
        Updating ffa646a..70c7eba
        Fast-forward
        file.txt | 1 +
        1 file changed, 1 insertion(+)
        ```

    * Let's check the log again. 
   
        ```
        $ git log
        commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:55:50 2017 -0400

            add second line

        commit ffa646af70ecac7b84b9b0f80da3246d921280bd
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:41:41 2017 -0400

            create file.txt

        commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:39:45 2017 -0400

            first commit
        (env) rwibawa1@ip-1-70-62-141:~/github/fork/git-test-1$
        ```

    * Yes, it has Coder1's latest changes. 
	

## Scenario 2: Sync upstream to specific branch in local repo

* Let's start again with Coder1 makes another change on his repo, commit his change and push to github

    ```
    $ vim file.txt

    $ git diff file.txt
    diff --git a/file.txt b/file.txt
    index 0b946aa..6c3eb35 100644
    --- a/file.txt
    +++ b/file.txt
    @@ -1,2 +1,3 @@
    first
    second
    +third

    $ git commit -m "add third line" file.txt
    [master 22443cf] add third line
    1 file changed, 1 insertion(+)

    $ git push
    Counting objects: 3, done.
    Compressing objects: 100% (2/2), done.
    Writing objects: 100% (3/3), 291 bytes | 0 bytes/s, done.
    Total 3 (delta 0), reused 0 (delta 0)
    To https://github.com/Coder1/git-test-1.git
    70c7eba..22443cf  master -> master

    $ git log
    commit 22443cf44425624bf2715feedb11e26ea9c6d934
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 12:36:07 2017 -0400

        add third line

    commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 10:55:50 2017 -0400

        add second line

    commit ffa646af70ecac7b84b9b0f80da3246d921280bd
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 10:41:41 2017 -0400

        create file.txt

    commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 10:39:45 2017 -0400

        first commit

    ```


* Then, Coder2 want to create a new feature

* Coder2 want to make sure his local repo has all latest Coder1 changes, but he also want to keep hist local repo master branch intact until he finish with all the changes. 

    * Coder2 double check his master branch git log, make sure no more update from last time

        ```
        $ git log
        commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:55:50 2017 -0400

            add second line

        commit ffa646af70ecac7b84b9b0f80da3246d921280bd
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:41:41 2017 -0400

            create file.txt

        commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:39:45 2017 -0400

            first commit
        ```

	  * Coder2 creates new branch in his local repo

        ```
        $ git checkout -b feature-1
        Switched to a new branch 'feature-1'
        $ git branch
        * feature-1
            master
        ```

	  * now Coder2 has new branch and now he works on branch feature-1
	

    * Before make any changes, Coder2 want to make sure this branch is sync with the upstream (Coder1's master repo)

        ```
        $ git fetch upstream
        remote: Counting objects: 3, done.
        remote: Compressing objects: 100% (2/2), done.
        remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
        Unpacking objects: 100% (3/3), done.
        From https://github.com/Coder1/git-test-1
            70c7eba..22443cf  master     -> upstream/master
        
        $ git merge upstream/master
        Updating 70c7eba..22443cf
        Fast-forward
        file.txt | 1 +
        1 file changed, 1 insertion(+)
        
        $ git log
        commit 22443cf44425624bf2715feedb11e26ea9c6d934
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 12:36:07 2017 -0400

            add third line

        commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:55:50 2017 -0400

            add second line

        commit ffa646af70ecac7b84b9b0f80da3246d921280bd
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:41:41 2017 -0400

            create file.txt

        commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 10:39:45 2017 -0400

            first commit
        ```
	
	  * Coder2 branch feature-1 now is in sync with Coder1 master repo
	

    * Since Coder2 a bit paranoid, so just in case, Coder2 want to make sure that his master branch is still intact and has no update from upstream repo

        * Coder2 temporarily switch to master branch and check git log

            ```
            $ git checkout master
            Switched to branch 'master'
            Your branch is ahead of 'origin/master' by 1 commit.
                (use "git push" to publish your local commits)
            ```

        * Check the log on Coder2's local repo master branch

            ```
            $ git log
            commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:55:50 2017 -0400

                add second line

            commit ffa646af70ecac7b84b9b0f80da3246d921280bd
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:41:41 2017 -0400

                create file.txt

            commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:39:45 2017 -0400

                first commit
            ```
	
	  * It looks good so far
   

## Scenario 3: Rollback to previous state

* Time for Coder2 to start developing new feature 

    * Coder2 switch back to feature-1 branch

    ```
    $ git checkout feature-1
    Switched to branch 'feature-1'

    $ git branch
    * feature-1
        master
    ```

* Coder2 start to make changes, commit it

	```
	$ vim file.txt
	$ vim file.txt
	$ git commit -m "add fourth line" file.txt
	[feature-1 f38c0d6] add fourth line
	 1 file changed, 1 insertion(+)
	```

* Coder2 realizes he doesn't like the change he made, and want to go back to the state before he made changes

    * Coder2 reset his local repo HEAD to the point when he synced his repo to upstream

        ```
        $ git reflog
        f38c0d6 HEAD@{0}: commit: add fourth line
        22443cf HEAD@{1}: checkout: moving from master to feature-1
        70c7eba HEAD@{2}: checkout: moving from feature-1 to master
        22443cf HEAD@{3}: merge upstream/master: Fast-forward
        70c7eba HEAD@{4}: checkout: moving from master to feature-1
        70c7eba HEAD@{5}: merge upstream/master: Fast-forward
        ffa646a HEAD@{6}: clone: from https://github.com/Coder2/git-test-1

        $ git reset 22443cf
        Unstaged changes after reset:
        M       file.txt
        
        $ git diff
        diff --git a/file.txt b/file.txt
        index 6c3eb35..9257c95 100644
        --- a/file.txt
        +++ b/file.txt
        @@ -1,3 +1,4 @@
        first
        second
        third
        +fourth (from fork)	
        ```
    

    * Coder2 check his local repo status

        ```
        $ git reflog
        22443cf HEAD@{0}: reset: moving to 22443cf
        f38c0d6 HEAD@{1}: commit: add fourth line
        22443cf HEAD@{2}: checkout: moving from master to feature-1
        70c7eba HEAD@{3}: checkout: moving from feature-1 to master
        22443cf HEAD@{4}: merge upstream/master: Fast-forward
        70c7eba HEAD@{5}: checkout: moving from master to feature-1
        70c7eba HEAD@{6}: merge upstream/master: Fast-forward
        ffa646a HEAD@{7}: clone: from https://github.com/Coder2/git-test-1


        $ git status
        On branch feature-1
        Changes not staged for commit:
            (use "git add <file>..." to update what will be committed)
            (use "git checkout -- <file>..." to discard changes in working directory)

            modified:   file.txt

        Untracked files:
            (use "git add <file>..." to include in what will be committed)

            file2.txt

        no changes added to commit (use "git add" and/or "git commit -a")
        ```


	  * The reset bring Coder1 local repo to the state before he made a commit of his change, but his change is still there.

    * Coder2 decides to do another reset but this time he want to discard everything including the changes and any untracked file

        * Option 1: Find the correct reflog ID and jump back to that ID

            ```
            $ git reflog
            22443cf HEAD@{0}: reset: moving to 22443cf
            f38c0d6 HEAD@{1}: commit: add fourth line
            22443cf HEAD@{2}: checkout: moving from master to feature-1
            70c7eba HEAD@{3}: checkout: moving from feature-1 to master
            22443cf HEAD@{4}: merge upstream/master: Fast-forward
            70c7eba HEAD@{5}: checkout: moving from master to feature-1
            70c7eba HEAD@{6}: merge upstream/master: Fast-forward
            ffa646a HEAD@{7}: clone: from https://github.com/Coder2/git-test-1

            $ git reset --hard 22443cf
            HEAD is now at 22443cf add third line
            (env) rwibawa1@ip-1-70-62-141:~/github/fork/git-test-1$ git status
            On branch feature-1
            Untracked files:
                (use "git add <file>..." to include in what will be committed)

                file2.txt

            nothing added to commit but untracked files present (use "git add" to track)

            $ git log
            commit 22443cf44425624bf2715feedb11e26ea9c6d934
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 12:36:07 2017 -0400

                add third line

            commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:55:50 2017 -0400

                add second line

            commit ffa646af70ecac7b84b9b0f80da3246d921280bd
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:41:41 2017 -0400

                create file.txt

            commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:39:45 2017 -0400

                first commit

            $ git reflog
            22443cf HEAD@{0}: reset: moving to 22443cf
            f38c0d6 HEAD@{1}: commit: add fourth line
            22443cf HEAD@{2}: checkout: moving from master to feature-1
            70c7eba HEAD@{3}: checkout: moving from feature-1 to master
            22443cf HEAD@{4}: merge upstream/master: Fast-forward
            70c7eba HEAD@{5}: checkout: moving from master to feature-1
            70c7eba HEAD@{6}: merge upstream/master: Fast-forward
            ffa646a HEAD@{7}: clone: from https://github.com/Coder2/git-test-1
            ```

        
        * Option 2: simply reset local repo HEAD to be the same as Upstream/Coder1 github repo HEAD

            ```
            $ git reset --hard upstream/master
            HEAD is now at 22443cf add third line

            $ git reflog
            22443cf HEAD@{0}: reset: moving to 22443cf
            f38c0d6 HEAD@{1}: commit: add fourth line
            22443cf HEAD@{2}: checkout: moving from master to feature-1
            70c7eba HEAD@{3}: checkout: moving from feature-1 to master
            22443cf HEAD@{4}: merge upstream/master: Fast-forward
            70c7eba HEAD@{5}: checkout: moving from master to feature-1
            70c7eba HEAD@{6}: merge upstream/master: Fast-forward
            ffa646a HEAD@{7}: clone: from https://github.com/Coder2/git-test-1
            
            $ git log
            commit 22443cf44425624bf2715feedb11e26ea9c6d934
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 12:36:07 2017 -0400

                add third line

            commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:55:50 2017 -0400

                add second line

            commit ffa646af70ecac7b84b9b0f80da3246d921280bd
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:41:41 2017 -0400

                create file.txt

            commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:39:45 2017 -0400

                first commit
            
            $ git status
            On branch feature-1
            Untracked files:
                (use "git add <file>..." to include in what will be committed)

                file2.txt

            nothing added to commit but untracked files present (use "git add" to track)
            ```


    * Great, now file.txt is back to the state before Coder2 made the change, but file2.txt which has not been tracked by git is still there.
	
    * Coder2 want to reset and remove the untracked file too. Basically make sure the state is the same as its upstream 

        ```
        $ git clean -f -d
        Removing file2.txt

        $ git status
        On branch feature-1
        nothing to commit, working directory clean
        ```

    * Great!, now everything is clean 


## Scenario 4: Pull request

* Coder2 makes some changes again, this time he will be ready to sync his changes to upstream repo/Coder1 github repo

    * Coder2 makes few changes 
    
        ```
        $ vim file.txt
        $ git commit -m "add 4th line" file.txt
        [feature-1 7b67a07] add 4th line
        1 file changed, 1 insertion(+)
        ```

    * The changes look good and now its ready to be push to Coder2 github repo

        ```
        $ git push -u origin feature-1
        Username for 'https://github.com': Coder2
        Password for 'https://Coder2@github.com':
        Counting objects: 9, done.
        Compressing objects: 100% (6/6), done.
        Writing objects: 100% (9/9), 818 bytes | 0 bytes/s, done.
        Total 9 (delta 0), reused 0 (delta 0)
        To https://github.com/Coder2/git-test-1
        * [new branch]      feature-1 -> feature-1
        Branch feature-1 set up to track remote branch feature-1 from origin.
        ```

* Meanwhile, Coder1 also makes some changes on his local repo and hist Github repo, which is the upstream repo of Coder2

	```
	$ git commit -m "add 5th line" file.txt
	[master 4eb350b] add 5th line
	 1 file changed, 1 insertion(+)

	$ git push
	Counting objects: 3, done.
	Compressing objects: 100% (2/2), done.
	Writing objects: 100% (3/3), 296 bytes | 0 bytes/s, done.
	Total 3 (delta 0), reused 0 (delta 0)
	To https://github.com/Coder1/git-test-1.git
	   22443cf..4eb350b  master -> master
	```


* Coder2 is ready to create a pull request to sync his commited changes to upstream/Coder1's Github repo

    * Re-sync with upstream first, to minimize conflict so Coder2 will make sure that his repo has all the latest update from the upstream/Coder1 Github repo

        ```
        $ git fetch upstream
        remote: Counting objects: 3, done.
        remote: Compressing objects: 100% (2/2), done.
        remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
        Unpacking objects: 100% (3/3), done.
        From https://github.com/Coder1/git-test-1
            22443cf..4eb350b  master     -> upstream/master
        
        $ git merge upstream/master
        Auto-merging file.txt
        CONFLICT (content): Merge conflict in file.txt
        Automatic merge failed; fix conflicts and then commit the result.
        ```

 * Ooops, automatic merge fails, time to manually fix this

    * check the file content that has files, and fix it

        ```
        $ git status
        On branch feature-1
        Your branch is up-to-date with 'origin/feature-1'.
        You have unmerged paths.
            (fix conflicts and run "git commit")

        Unmerged paths:
            (use "git add <file>..." to mark resolution)

            both modified:   file.txt

        no changes added to commit (use "git add" and/or "git commit -a")

        $ cat file.txt
        first
        second
        third
        <<<<<<< HEAD
        fourth from fork
        =======
        five
        >>>>>>> upstream/master

        $ vim file.txt

        $ cat file.txt
        first
        second
        third
        fourth from fork
        five


    * check the status again

        ```
        $ git status
        On branch feature-1
        Your branch is up-to-date with 'origin/feature-1'.
        You have unmerged paths.
            (fix conflicts and run "git commit")

        Unmerged paths:
            (use "git add <file>..." to mark resolution)

            both modified:   file.txt

        no changes added to commit (use "git add" and/or "git commit -a")
        ```


    * merge the changes from upstream to Coder2 changes on his local repo

        ```
        $ git add file.txt

        $ git commit -m "manual merge fix" file.txt
        fatal: cannot do a partial commit during a merge.

        $ git commit -i -m "add 4th line" file.txt
        [feature-1 cbf8373] add 4th line

        $ git status
        On branch feature-1
        Your branch is ahead of 'origin/feature-1' by 2 commits.
            (use "git push" to publish your local commits)
        nothing to commit, working directory clean

            $ git log
            commit cbf8373915b5210fd8b062f3d69d4703b75373cb
            Merge: 7b67a07 4eb350b
            Author: Coder2 <Coder2@gajahmail.com>
            Date:   Mon Jun 5 13:41:53 2017 -0400

                add 4th line

            commit 4eb350bcc332601defe0192adf1081ee2bda89c0
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 13:36:34 2017 -0400

                add 5th line

            commit 7b67a0743e75d02da44deeb6acbd5459e9ba8679
            Author: Coder2 <Coder2@gajahmail.com>
            Date:   Mon Jun 5 13:30:53 2017 -0400

                add 4th line

            commit 22443cf44425624bf2715feedb11e26ea9c6d934
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 12:36:07 2017 -0400

                add third line

            commit 70c7ebad93f06872b16243ad5a9e341ea3ddfa02
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:55:50 2017 -0400

                add second line

            commit ffa646af70ecac7b84b9b0f80da3246d921280bd
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:41:41 2017 -0400

                create file.txt

            commit 8f61c17f443dfab4ed1e2761749967b6b200dac6
            Author: Coder1 <Coder1@gajahmail.com>
            Date:   Mon Jun 5 10:39:45 2017 -0400

                first commit
            ```

    
* Everything looks good, Coder2 now is creating pull request from github website

* The pull request is approved and merged to Coder1 Github repo master branch


## Scenario 5: Re-sync the master after merging pull request

* Coder2 move back to his master branch and sync it with the upstream master to get all the update including his pull request

    * Coder2 switch to master branch
    
        ```
        $ git checkout master
        Switched to branch 'master'
        Your branch is ahead of 'origin/master' by 1 commit.
        (use "git push" to publish your local commits)

        $ git branch
        feature-1
        * master
        ```

    * Coder2 pull Coder1 Github repo latest changes and merge it to local repo

        ``` 
        $ git fetch upstream
        remote: Counting objects: 1, done.
        remote: Total 1 (delta 0), reused 1 (delta 0), pack-reused 0
        Unpacking objects: 100% (1/1), done.
        From https://github.com/Coder1/git-test-1
        4eb350b..069465b  master     -> upstream/master

        $ git merge upstream/master
        Updating 70c7eba..069465b
        Fast-forward
        file.txt | 3 +++
        1 file changed, 3 insertions(+)
        ```

    * Coder2 check the commit log 

        ```
        $ git log -n 3
        commit 069465b0c0b32ab8e41194451639af54ee0a1b85
        Merge: 4eb350b cbf8373
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 14:16:46 2017 -0400

            Merge pull request #1 from Coder2/feature-1

            Feature 1

        commit cbf8373915b5210fd8b062f3d69d4703b75373cb
        Merge: 7b67a07 4eb350b
        Author: Coder2 <Coder2@gajahmail.com>
        Date:   Mon Jun 5 13:41:53 2017 -0400

            add 4th line

        commit 4eb350bcc332601defe0192adf1081ee2bda89c0
        Author: Coder1 <Coder1@gajahmail.com>
        Date:   Mon Jun 5 13:36:34 2017 -0400

            add 5th line
        ```


* Meanwhile, Coder1 as the upstream owner also want to sync his own local repo to the latest version of his Github repo after merging with Coder2 changes.

    ```
    $ git pull
    remote: Counting objects: 7, done.
    remote: Compressing objects: 100% (5/5), done.
    remote: Total 7 (delta 0), reused 7 (delta 0), pack-reused 0
    Unpacking objects: 100% (7/7), done.
    From https://github.com/Coder1/git-test-1
       4eb350b..069465b  master     -> origin/master
    Updating 4eb350b..069465b
    Fast-forward
     file.txt | 1 +
     1 file changed, 1 insertion(+)

    $ git log -n 5
    commit 069465b0c0b32ab8e41194451639af54ee0a1b85
    Merge: 4eb350b cbf8373
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 14:16:46 2017 -0400

        Merge pull request #1 from Coder2/feature-1

        Feature 1

    commit cbf8373915b5210fd8b062f3d69d4703b75373cb
    Merge: 7b67a07 4eb350b
    Author: Coder2 <Coder2@gajahmail.com>
    Date:   Mon Jun 5 13:41:53 2017 -0400

        add 4th line

    commit 4eb350bcc332601defe0192adf1081ee2bda89c0
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 13:36:34 2017 -0400

        add 5th line

    commit 7b67a0743e75d02da44deeb6acbd5459e9ba8679
    Author: Coder2 <Coder2@gajahmail.com>
    Date:   Mon Jun 5 13:30:53 2017 -0400

        add 4th line

    commit 22443cf44425624bf2715feedb11e26ea9c6d934
    Author: Coder1 <Coder1@gajahmail.com>
    Date:   Mon Jun 5 12:36:07 2017 -0400

        add third line

    ```



