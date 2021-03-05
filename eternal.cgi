#!/usr/bin/perl -T
# -*- CPerl -*-
use Modern::Perl '2015';

#use strict;
###
# https://www.jwz.org/blog/2021/03/double-march/
use Date::Parse;
use POSIX;
use CGI qw(:standard start_ul *table -utf8);
use CGI::Carp qw(fatalsToBrowser);
use Template;
use FindBin qw/$Bin/;
use utf8;
use DateTime::Calendar::FrenchRevolutionary;
binmode( STDOUT, ":utf8" );

sub commify {
    my $text = reverse $_[0];
    $text =~ s/(\d\d\d)(?=\d)(?!\d*\.)/$1,/g;
    return scalar reverse $text;
}

my $query = new CGI;
my $tt    = Template->new(
    {   INCLUDE_PATH => "$Bin/templates",
        ENCODING     => 'UTF-8'
    }
);
my $test    = $query->param('t')       || '';
my $console = $query->param('console') || '';
my $now;
if ($test) {
    $now = 1614798423;
}
else {
    $now = time;
}
my $frc = DateTime::Calendar::FrenchRevolutionary->from_epoch(
    epoch => ( $now + 9 * 60 + 21 ) );
my $dt      = DateTime->from_epoch( epoch => $now );
my $weekday = $dt->day_name;                           # strftime( "%A", @t );
my $wd      = $dt->day_abbr;
my $mar1      = DateTime->new( year => 2020, month => 3, day => 1 );
my $sep1      = DateTime->new( year => 1993, month => 9, day => 1 );
my $march_day = commify( int( 1 + ( $dt->jd - $mar1->jd ) ) );
my $sep_day   = commify( int( 1 + ( $dt->jd - $sep1->jd ) ) );

my $bmt = DateTime->from_epoch( epoch => $now, time_zone => "+0100" );
my @utc_plus_one = gmtime( $now + 3600 );
my $beats        = int( ( $bmt->hour * 3600 + $bmt->minute * 60 ) / 86.4 );
my %data         = (
    meta     => { page_title => '𝖊 𝖙 𝖊 𝖗 𝖓 𝖆 𝖑' },
    calendar => {
        gregorian => $dt->strftime("%e %B %Y"),
        weekday   => $weekday,
        march     => "$march_day March 2020",
        september => "$sep_day September 1993",
        fr_rev    => $frc->strftime("%A, %d %B %EY (%EJ)"),
        julian    => $dt->jd,
    },
    time => {
        utc    => $dt->strftime("%H:%M:%S UTC"),
        fr_rev => $frc->strftime("%H:%M:%S"),
        beats  => $beats,
    },
    console => {
        wd   => $wd,
        greg => $dt->strftime("%e %b %Y"),
        mar  => "$march_day Mar 2020",
        sep  => "$sep_day Sep 1993",
        frc  => $frc->strftime("%A, %e %B %EY"),
    },
);
my $out = '';

if ($console) {
    $tt->process( "console.tt", \%data, \$out ) or die $tt->error;
}
else {
    $out = header( { -type => 'text/html', -charset => 'utf-8' } );
    $tt->process( "eternal.tt", \%data, \$out ) or die $tt->error;

}
print $out;
