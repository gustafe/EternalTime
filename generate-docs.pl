#! /usr/bin/env perl
use Modern::Perl '2015';
###
use utf8;
use warnings qw(FATAL utf8);    # fatalize encoding glitches
use open qw(:std :utf8);        # undeclared streams in UTF-8
use DateTime;
use Template;
use FindBin qw/$Bin/;

my $now = time();
my $dt_now
    = DateTime->from_epoch( epoch => $now, time_zone => 'Europe/Stockholm' );

my %data = (
    meta => {
        page_title    => 'a b o u t  e t e r n a l',
        generate_time => $dt_now->strftime('%Y-%m-%d %H:%M:%S%z'),
    }
);

my $tt = Template->new(
    {   ENCODING     => 'UTF-8',
        INCLUDE_PATH => "$Bin/templates"
    }
);

$tt->process(
    'about.tt', \%data,
    '/home/gustaf/public_html/eternal/about.html',
    { binmode => ':utf8' }
) || die $tt->error;
