#!/usr/bin/perl

use strict;
use warnings;
use Template;

my $template = Template->new({
  INCLUDE_PATH => '/usr/share/elephant-shed/template',
  POST_CHOMP => 1,
});

print "Content-type: text/html\n\n";

$template->process('header.html', {
  SERVER_NAME => $ENV{SERVER_NAME},
  REMOTE_USER => $ENV{REMOTE_USER},
  TITLE => "$ENV{REQUEST_URI} - PostgreSQL",
  HEADLINE => $ENV{REQUEST_URI},
}) or die $template->error();
