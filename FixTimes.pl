#!/usr/bin/perl
use warnings;
use strict;

## Excel screwed up the timestamps in some of the data files, leaving only the minutes and seconds
## Luckily, the dates and starting hours were known from the filenames, so this script was used to 
## parse through each data file and print a new version with correctly formatted timestamps

# get correct day and starting hour from filename (month is always April 2017)
my $file = shift @ARGV;
print STDERR "Fixing bad timestamps for $file...\n";
(my $substring = $file) =~ s/.*Apr_//;
(my $day = $substring) =~ s/_.*//;
(my $startTime = $substring) =~ s/^\d\d_//;
$startTime =~ s/^(\d\d\d\d).*/$1/;
(my $hour = $startTime) =~ s/\d\d$//;
(my $earliestMinute = $startTime) =~ s/^\d\d//;

# open file, print header line, then re-print data lines with timestamp fixed
open my $IN, '<', $file or die $!;
my $header = <$IN>;
print $header;
while (my $line = <$IN>) {
	my @fields = split /\t/, $line;
	my $badTime = $fields[1];
	my ($minutes, $seconds) = split /:/, $badTime;
	# have to go to next hour when the minute gets smaller (e.g., minute 59 -> minute 0)
	if ($minutes < $earliestMinute) {
		print STDERR "Warning: Rolled over to next hour on line $.\n";
		$earliestMinute = $minutes; # this is fine because task duration is never > 60 minutes, so can't roll to a new hour more than once
		$hour++;
	}
	my $goodTime = "2017-04-$day $hour:$minutes:$seconds";
	$fields[1] = $goodTime;
	my $newOutput = join "\t", @fields;
	print $newOutput;
}
close $IN;