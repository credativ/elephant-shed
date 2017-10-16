#!/usr/bin/perl

use strict;
use warnings;
use PgCommon;
use Template;

my $template = Template->new({
  INCLUDE_PATH => '/usr/share/elephant-shed/template',
  POST_CHOMP => 1,
});

print "Content-type: text/html\n\n";

$template->process('error.html', {
  SERVER_NAME => $ENV{SERVER_NAME},
  REMOTE_USER => $ENV{REMOTE_USER},
  TITLE => "$ENV{REDIRECT_STATUS} - PostgreSQL",
  HEADLINE => "Error $ENV{REDIRECT_STATUS}",
  REDIRECT_STATUS => $ENV{REDIRECT_STATUS},
  REDIRECT_SCRIPT_URI => $ENV{REDIRECT_SCRIPT_URI},
}) or die $template->error();
