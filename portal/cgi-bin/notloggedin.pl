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

$template->process('notloggedin.html', {
  SERVER_NAME => $ENV{SERVER_NAME},
  TITLE => "PostgreSQL Appliance",
  HEADLINE => "PostgreSQL Appliance",
}) or die $template->error();
