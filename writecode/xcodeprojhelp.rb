require 'xcodeproj'

def addreferences(projpath,projname,filename,filepath)

    project = Xcodeproj::Project.open(projpath)

    targetIndex = 0
    targetIndex_clean = 0

    project.targets.each_with_index do |target, index|
        if target.name  == projname
            targetIndex = index
        end

        if target.name  == projname + "_CLEAN"
            targetIndex_clean = index
        end
    end

    target = project.targets[targetIndex]
    target_clean = project.targets[targetIndex_clean]

    #找到要插入的group (参数中true表示如果找不到group，就创建一个group)
    group = project.main_group.find_subpath(File.join(projname),true)
    
    #set一下sorce_tree
    group.set_source_tree('SOURCE_ROOT')

    #向group中增加文件引用（.h文件只需引用一下，.m引用后还需add一下）
    h_path = filepath+filename+".h"
    file_ref = group.new_reference(h_path)
  
    m_path = filepath+filename+".m"
    file_ref = group.new_reference(m_path)
    target.add_file_references([file_ref])
    target_clean.add_file_references([file_ref])
    project.save
end

addreferences(ARGV[0],ARGV[1],ARGV[2],ARGV[3])