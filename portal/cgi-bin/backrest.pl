#!/usr/bin/perl

use strict;
use warnings;
use Template;
use CGI;
use CGI::Carp 'fatalsToBrowser';
use Data::Dumper;

my $q = CGI->new();
my $get_cluster = $q->param('cluster') // '';

my $template_path = '/usr/share/elephant-shed/template';
my $page = 'backrest.html';

my $template = Template->new({
  INCLUDE_PATH => $template_path,
  POST_CHOMP => 1,
});

print "Content-type: text/html\n\n";

my $directory = '/var/www/html/pgbackrest';
my @backup_files;
my %backups;
opendir (DIR, $directory) or die $!;
while (my $file = readdir(DIR)) {
    # We always want to list files with "backup" or "log" suffix.
    next unless ($file =~ m/.*\.(backup|log)/);
    # If the GET parameter "cluster" is given we want to filter out
    # all other clusters.
    next unless ($file =~ m/$get_cluster(\.(backup|log))?/);
    push @backup_files, $file;

    open (FILE, join "/",$directory,$file) || die "Could not open \"$file\", $!";
    my $content = join '', <FILE>;
    $backups{$file} = $content;
}

$template->process($page, {
  SERVER_NAME => $ENV{SERVER_NAME},
  REMOTE_USER => $ENV{REMOTE_USER},
  TITLE => "Backups",
  HEADLINE => "Backups",
  BACKUP_FILES => \@backup_files,
  BACKUPS => \%backups,
}) or die $template->error();
