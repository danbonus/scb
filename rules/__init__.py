from rules import FirstEntry, Registered, NotRegistered, IsWriter, IsAdmin, IsMessageNotEmpty

rules = [
    FirstEntry.FirstEntry,
    Registered.Registered,
    NotRegistered.NotRegistered,
    IsWriter.IsWriter,
    IsAdmin.IsAdmin,
    IsMessageNotEmpty.IsMessageNotEmpty
]