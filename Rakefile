require "csv"
require "rake/clean"

datasets = CSV.table "datasets.csv"
segmentation_datasets = CSV.table "segmentation_datasets.csv"

namespace :segmentation do

  segmentation_datasets.each do |dataset|

    desc "segment #{dataset[:reconstruction]}"
    file dataset[:segmentation] => ["segment.py", "segment_macro.py", dataset[:reconstruction]] do |f|
      mkdir_p dataset[:segmentation]
      sh "rm -f #{f.name}/*.tif"
      sh "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
    end
  end

  desc "segment all"
  task :all => segmentation_datasets[:segmentation]

end

namespace :test do
  # test with a small file
  datasets.each do |dataset|

    desc "calculate distance ridge of #{dataset[:stitched]} with fiji"
    file dataset[:distance_ridge] => ["distance_ridge.py", "distance_ridge_macro.py", dataset[:stitched]] do |f|
      mkdir_p dataset[:distance_ridge]
      sh "python #{f.prerequisites[0]} #{f.prerequisites[2]} #{f.name}"
    end

    desc "compress local thickness of #{dataset[:name]}"
    file dataset[:local_thickness_compressed] => ["compress.py", dataset[:local_thickness_volume]] do |f|
      #sh "python #{f.prerequisites[0]} --chunks 25 #{f.prerequisites[1]} #{f.name}"
      sh "python #{f.prerequisites[0]} #{f.prerequisites[1]} #{f.name}"
    end

    desc "calculate kde of #{dataset[:name]}"
    file dataset[:local_thickness_kde] => ["thickmap2kde.R", dataset[:local_thickness_compressed]] do |f|
      sh "./#{f.prerequisites[0]} #{f.prerequisites[1]} #{f.name}"
    end

    desc "plot local thickness of #{dataset[:name]}"
    file dataset[:local_thickness_plot] => ["plot_single.R", dataset[:local_thickness_kde]] do |f|
      sh "./#{f.prerequisites[0]} --title #{dataset[:name]} #{f.prerequisites[1]} #{f.name}"
    end

  end
end
