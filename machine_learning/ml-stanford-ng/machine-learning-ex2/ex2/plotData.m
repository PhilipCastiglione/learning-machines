function plotData(X, y)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.

% Create New Figure
figure; hold on;

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the positive and negative examples on a
%               2D plot, using the option 'k+' for the positive
%               examples and 'ko' for the negative examples.
%
admitted_idxs = find(y == 1);
rejected_idxs = find(y == 0);

exam_1_admitted = X(admitted_idxs, 1);
exam_2_admitted = X(admitted_idxs, 2);

exam_1_rejected = X(rejected_idxs, 1);
exam_2_rejected = X(rejected_idxs, 2);

plot(exam_1_admitted, exam_2_admitted, 'b+', 'markersize', 5);
plot(exam_1_rejected, exam_2_rejected, 'ro', 'markersize', 5);
% =========================================================================



hold off;

end
