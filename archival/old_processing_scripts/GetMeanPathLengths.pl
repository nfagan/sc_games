#!/usr/bin/perl
use strict;
use warnings;

my $file = shift @ARGV;
open my $IN, '<', $file or die $!;
$/ = undef;
my $fileContent = <$IN>;
close $IN;
my @lines = split /[\n\r]+/, $fileContent;
shift @lines while ($lines[0] =~ /^#/);
my $headerLine = shift @lines;
my @headerCols = split /\t/, $headerLine;
my ($trialCol, $xHandCol, $yHandCol, $timeCol);
my $colNum = 0;
for (@headerCols) {
	if ($_ eq 'Trial') {
		$trialCol = $colNum;
	} elsif ($_ eq 'X_hand' || $_ eq 'X_wand') {
		$xHandCol = $colNum;
	} elsif ($_ eq 'Y_hand' || $_ eq 'Y_wand') {
		$yHandCol = $colNum;
	} elsif ($_ eq 'Time') {
		$timeCol = $colNum;
	}
	$colNum++;
}

my %pathLengths;
for my $line (@lines) {
	next if ($line =~ /^#/);
	my @fields = split /\t/, $line;
	my $trialNum = $fields[$trialCol];
	if (! exists $fields[$xHandCol] || ! exists $fields[$yHandCol]) {
		print STDERR "Warning: Missing hand location in file $file at time $fields[$timeCol].\n";
		next;
	}
	my $xHand = $fields[$xHandCol];
	my $yHand = $fields[$yHandCol];
	if (exists $pathLengths{$trialNum}{'previous'} && $pathLengths{$trialNum}{'previous'} ne "$xHand,$yHand") {
		$pathLengths{$trialNum}{'previous'} = "$xHand,$yHand";
		$pathLengths{$trialNum}{'total'}++;
	} else {
		$pathLengths{$trialNum}{'previous'} = "$xHand,$yHand";
	}
}


my $firstHalfTotal = 0;
my $secondHalfTotal = 0;
my $numFirstHalfTrials = 0;
my $numSecondHalfTrials = 0;
for (1 .. 15) {
	next unless (exists $pathLengths{$_}{'total'});
	$firstHalfTotal += $pathLengths{$_}{'total'};
	$numFirstHalfTrials++;
}

for (16 .. 30) {
	next unless (exists $pathLengths{$_}{'total'});
	$numSecondHalfTrials++;
	$secondHalfTotal += $pathLengths{$_}{'total'};
}

my $firstHalfMean = $firstHalfTotal/15;
my $secondHalfMean = 'NA';
if ($numSecondHalfTrials > 0) {
	$secondHalfMean = $secondHalfTotal/$numSecondHalfTrials;
}
my $totalMean = ($firstHalfTotal + $secondHalfTotal)/($numFirstHalfTrials + $numSecondHalfTrials);
#print "$file\t$firstHalfMean\t$secondHalfMean\t$totalMean\n";

my $totalNumTrials = $numFirstHalfTrials + $numSecondHalfTrials;
my $totalPath = $firstHalfTotal + $secondHalfTotal;

$file =~ s/.*\///;
print "$file\t$totalPath\t$totalNumTrials\n";
