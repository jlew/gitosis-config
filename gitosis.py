#########################################################################
## This software is in the public domain, furnished "as is", without   ##
## technical support, and with no warranty, express or implied, as to  ##
## its usefulness for any purpose.                                     ##
##                                                                     ##
## gitosis.py                                                          ##
## A simple script for managing gitosis config files                   ##
##                                                                     ##
## https://gitorious.org/jlew/gitosis-config                           ##
##                                                                     ##
## Author: Justin Lewis <jlew.blackout@gmail.com>                      ##
#########################################################################
import ConfigParser

class gitosis:
    def __init__(self, filename=""):
        self.config = ConfigParser.ConfigParser()
        self.filename = filename

        if filename:
            f = open(filename, 'r')
            self.config.readfp(f)
            f.close()

        else:
            self.config.add_section("gitosis")
            self.config.set("gitosis","daemon","yes")
            self.config.set("gitosis","gitweb","yes")

    def save(self):
        if self.filename:
            self.write( self.filename )

    def write(self, filename=""):
        f = open( filename, 'w' )
        self.config.write(f)
        f.close()

    def add_repo(self, name, desc, owner):
        # Add repo section
        rep_section = "repo %s" % name
        self.config.add_section(rep_section)
        self.config.set(rep_section, 'owner', owner)
        self.config.set(rep_section, 'description', desc)

        # Add user access section
        grp_section = "group repo_%s" % name
        self.config.add_section(grp_section)
        self.config.set(grp_section, 'members', owner)
        self.config.set(grp_section, 'writable', rep_section)

    def rem_repo(self, name):
        self.config.remove_section("repo %s" % name)
        self.config.remove_section("group repo_%s" % name)

    def add_access(self, repo, user):
        grp_section = "group repo_%s" % repo
        users = self.config.get(grp_section, 'members').split(" ")
        users.append( user )
        self.config.set(grp_section, 'members', ' '.join(users))

    def rem_access(self, repo, user):
        grp_section = "group repo_%s" % repo
        users = self.config.get(grp_section, 'members').split(" ")
        users.remove(user)
        self.config.set(grp_section, 'members', ' '.join(users))

    def show_access(self, repo):
        grp_section = "group repo_%s" % repo
        return self.config.get(grp_section, 'members').split(" ")

    def set_private(self, repo):
        repo_section = "repo %s" % repo
        self.config.set(repo_section, "daemon", "no")
        self.config.set(repo_section, "gitweb", "no")

    def set_public(self, repo):
        repo_section = "repo %s" % repo
        self.config.remove_option(repo_section, "daemon")
        self.config.remove_option(repo_section, "gitweb")

    def is_public(self, repo):
        repo_section = "repo %s" % repo
        return not self.config.has_option(repo_section, "gitweb")


if __name__ == "__main__":


    def add_repo(option, opt_str, value, parser):
            name, desc, owner = value
            g = gitosis( parser.values.file )
            g.add_repo( name, desc, owner )
            g.save()

    def rem_repo(option, opt_str, value, parser):
        g = gitosis(parser.values.file)
        g.rem_repo(value)
        g.save()

    def add_usr(option, opt_str, value, parser):
            repo, user = value
            g = gitosis( parser.values.file )
            g.add_access( repo, user )
            g.save()

    def rem_usr(option, opt_str, value, parser):
            repo, user = value
            g = gitosis( parser.values.file )
            g.rem_access( repo, user )
            g.save()


    def set_priv(option, opt_str, value, parser):
            g = gitosis( parser.values.file )
            g.set_private( value )
            g.save()

    def set_pub(option, opt_str, value, parser):
            g = gitosis( parser.values.file )
            g.set_public( value )
            g.save()

    def show_acl(option, opt_str, value, parser):
            g = gitosis( parser.values.file )
            print " ".join(g.show_access(value))


    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", default="gitosis.conf")
    parser.add_option("--add-repo", action="callback", callback=add_repo,
                      type="string", nargs=3, help="REPO DESCRIPTION OWNER",
                      dest="")

    parser.add_option("--rem-repo", action="callback", callback=rem_repo,
                      type="string", nargs=1, help="REPO", dest="")

    parser.add_option("--add-user", action="callback", callback=add_usr,
                      type="string", nargs=2, help="REPO USER", dest="")

    parser.add_option("--rem-user", action="callback", callback=rem_usr,
                      type="string", nargs=2, help="REPO USER", dest="")

    parser.add_option("--show-access", action="callback", callback=show_acl,
                      type="string", nargs=1, help="REPO", dest="")

    parser.add_option("--set-private", action="callback", callback=set_priv,
                      type="string", nargs=1, help="REPO", dest="")

    parser.add_option("--set-public", action="callback", callback=set_pub,
                      type="string", nargs=1, help="REPO", dest="")
    parser.parse_args()
