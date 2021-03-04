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
my $test = $query->param('t') || '';
my $now;
if ($test) {
    $now = 1614798423;
}
else {
    $now = time;
}

my @t   = gmtime($now);
my $frc = DateTime::Calendar::FrenchRevolutionary->from_epoch(
    epoch => ( $now + 9 * 60 + 21 ) );
my $dt = DateTime->from_epoch( epoch => $now );
my $weekday = strftime( "%A", @t );
my $march_day = commify(
    int(1 + 0.5 + (
            (         str2time( strftime( "%Y-%m-%d 3:00", @t ) )
                    - str2time("2020-03-01 3:00")
            ) / ( 60 * 60 * 24 )
        )
    )
);
my $sep_day = commify(
    int(1 + 0.5 + (
            (         str2time( strftime( "%Y-%m-%d 3:00", @t ) )
                    - str2time("1993-09-01 3:00")
            ) / ( 60 * 60 * 24 )
        )
    )
);

my @utc_plus_one = gmtime( $now + 3600 );

my $beats = sprintf(
    "%d",
    (   strftime( "%M", @utc_plus_one ) * 60
            + ( strftime( "%H", @utc_plus_one ) * 3600 )
    ) / 86.4
);
my %data = (
    meta     => { page_title => 'e t e r n a l' },
    calendar => {
        gregorian => strftime( "%A, %e %B %Y\n", @t ),
        march     => "$weekday, $march_day March 2020",
        september => "$weekday, $sep_day September 1993",
		 fr_rev    => $frc->strftime("%A, %d %B %EY (%EJ)"),
		 julian => $dt->jd,
    },
    time => {
        utc    => strftime( "%H:%M:%S UTC", @t ),
        fr_rev => $frc->strftime("%H:%M:%S"),
        beats  => $beats
    },
);
my $out = header( { -type => 'text/html', -charset => 'utf-8' } );
$tt->process( "eternal.tt", \%data, \$out ) or die $tt->error;
print $out;
