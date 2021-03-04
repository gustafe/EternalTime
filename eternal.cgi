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
use utf8;
use DateTime::Calendar::FrenchRevolutionary;
binmode (STDOUT, ":utf8");

sub commify {
    my $text = reverse $_[0];
    $text =~ s/(\d\d\d)(?=\d)(?!\d*\.)/$1,/g;
    return scalar reverse $text;
}



my $query = new CGI;
my $test = $query->param('t') || '';
my $now;
if ($test ) {
    $now = 1614798423
} else {
    $now = time;
}

my @t=gmtime( $now );
my $frc = DateTime::Calendar::FrenchRevolutionary->from_epoch(epoch=>( $now + 9*60 + 21));

my $weekday = strftime("%A",@t);
my $march_day = commify(int  (1 + 0.5 + ((str2time (strftime ("%Y-%m-%d 3:00", @t)) -
	       str2time ("2020-03-01 3:00")) /(60*60*24))));
my $sep_day = commify(int
  (1 + 0.5 + ((str2time (strftime ("%Y-%m-%d 3:00", @t)) -
	       str2time ("1993-09-01 3:00")) /(60*60*24))))	       		;

my @utc_plus_one = gmtime($now+3600);

my $beats = sprintf( "%d",(strftime( "%M", @utc_plus_one) * 60  + ( strftime("%H", @utc_plus_one) * 3600 )) / 86.4);


charset('utf-8');
print header();
print start_html(
    -title => "ETERNAL",
    -lang  => 'en-US',
     -head  => [

     meta({-name=>"viewport",-content=>"width=device-width, initial-scale=1"}),
    #     Link(
    #         {
    #             -rel   => 'stylesheet',
    #             -type  => 'text/css',
    #             -media => 'all',
    #             -href  => 'http://gerikson.com/stylesheets/twitterblog.css'
    #         }
    #     )
 ]
);

print "<center>";
print h1("e t e r n a l");

print p({-style=>"color:red; text-align:center"}, "test input epoch=$now") if $test;

print h2( "The date is");
# normal
print h1(strftime("%A, %e %B %Y\n", @t));
# eternal March
print h1("$weekday, $march_day March 2020");
# eternal September
print h1("$weekday, $sep_day September 1993");
# French Revolutionary 
print h1($frc->strftime("%A, %d %B %EY (%EJ)"));


print h2("The time is");
print h1(strftime("%H:%M:%S UTC",@t));
print h1($frc->strftime("%H:%M:%S"));
print h1('@'.	 $beats);

print p(a({-href=>"http://gerikson.com/eternal/about.html"},"about"));
print "</center>";
print end_html();
