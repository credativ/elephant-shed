#!/usr/bin/perl

use strict;
use warnings;
use PgCommon;
use Template;

my $pgbadgerdir = "/var/lib/pgbadger";
my $backupstatusdir = "/var/www/html/pgbackrest";

# get PostgreSQL cluster information
my @clusters;
foreach my $version (get_versions()) {
  foreach my $cluster (get_version_clusters($version)) {
    my %info = cluster_info($version, $cluster);
    $info{version} = $version;
    $info{cluster} = $cluster;
    $info{owner} = (getpwuid $info{'owneruid'})[0];

    # pgbadger report
    if (-e "$pgbadgerdir/$version-$cluster/LAST_PARSED") {
      $info{pgbadger} = "/pgbadger/$version-$cluster/";
    }

    # pgbackrest status
    if (-e "$backupstatusdir/$version-$cluster.backup") {
      $info{backup} = "/pgbackrest/$version-$cluster.backup";
    }

    push @clusters, \%info;
  }
}

my $template = Template->new({
  INCLUDE_PATH => '/usr/share/elephant-shed/template',
  POST_CHOMP => 1,
});

print "Content-type: text/html\n\n";

$template->process('portalmenu.html', {
  CLUSTERS => \@clusters,
  SERVER_NAME => $ENV{SERVER_NAME},
  REMOTE_USER => $ENV{REMOTE_USER},
}) or die $template->error();
