#!/usr/bin/perl

use strict;
use warnings;
use Template;

my $template = Template->new({
  INCLUDE_PATH => '/usr/share/elephant-shed/template',
  POST_CHOMP => 1,
});

print "Content-type: text/html\n\n";

$template->process('footer.html', {
}) or die $template->error();
