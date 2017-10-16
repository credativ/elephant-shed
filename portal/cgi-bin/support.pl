#!/usr/bin/perl

use strict;
use warnings;
use Template;

my $template_path = '/usr/share/elephant-shed/template';
my $support_page = 'support.html';


my $template = Template->new({
  INCLUDE_PATH => $template_path,
  POST_CHOMP => 1,
});

print "Content-type: text/html\n\n";

if (-f $template_path . '/support.partner.html') {
    $support_page = 'support.partner.html';
}

$template->process($support_page, {
  SERVER_NAME => $ENV{SERVER_NAME},
  REMOTE_USER => $ENV{REMOTE_USER},
  TITLE => "Support - PostgreSQL",
  HEADLINE => "PostgreSQL Support",
}) or die $template->error();
